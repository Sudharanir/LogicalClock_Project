from concurrent import futures
import multiprocessing
import time
import json

import grpc
import example_pb2
import example_pb2_grpc

class Branch(example_pb2_grpc.RPCServicer):
    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the local clock of the branch
        self.clock = 1

    # receives request from customer, process the request and sends back the response
    def MsgDelivery(self, request, context):
        # select the branch process with ID equls to customer
        for x in range(len(self.branches)) :
            if self.branches[x].id == request.id :
                branch = self.branches[x]
                break

        self = branch

        response = example_pb2.Response()
        response.id = request.id

        clockResponse = example_pb2.ClockResponse()

        for x in range(len(request.events)) :
            recvDict = example_pb2.Recv()

            event = request.events[x]
            reqType = event.interface
            recvDict.interface = reqType

            if reqType == 'query' :
                recvDict.money = QueryInterface(self)
                recvDict.result = 'success'
            elif reqType == 'deposit' :
                clockResponse.id = event.id
                recvDict.result = DepositInterface(self, event, request.clock, clockResponse.data)
            elif reqType == 'withdraw' :
                clockResponse.id = event.id
                recvDict.result = WithdrawInterface(self, event, request.clock, clockResponse.data)

            response.recv.append(recvDict)

        return clockResponse

# happens when the Branch process receives a request from the Customer process
def Event_Request(self, remoteClock, name, responseList) :
    # branch process selects the larger value from both the clocks and increments one
    self.clock = max(self.clock, remoteClock) + 1

    eventResponse = example_pb2.EventExecuted()
    eventResponse.id = self.id
    eventResponse.name = name
    eventResponse.clock = self.clock

    responseList.append(eventResponse)

# happens when the Branch process executes the event
def Event_Execute(self, event, name, responseList) :
    # branch process increments one from its local clock
    self.clock = self.clock + 1

    eventResponse = example_pb2.EventExecuted()
    eventResponse.id = self.id
    eventResponse.name = name
    eventResponse.clock = self.clock

    responseList.append(eventResponse)

# happens when the branch process receives the propagation request
def Propagate_Request(self, remoteClock, name, responseList) :
    # branch process selects the larger value from both the clocks and increments one
    self.clock = max(self.clock, remoteClock) + 1

    eventResponse = example_pb2.EventExecuted()
    eventResponse.id = self.id
    eventResponse.name = name
    eventResponse.clock = self.clock

    responseList.append(eventResponse)

# happens when the Branch process executes the propagation request event
def Propogate_Execute(self, name, responseList) :
    # branch process increments one from its local clock
    self.clock = self.clock + 1

    eventResponse = example_pb2.EventExecuted()
    eventResponse.id = self.id
    eventResponse.name = name
    eventResponse.clock = self.clock

    responseList.append(eventResponse)

# happens when the Branch process receives the result of propagation execute
def Propogate_Response(self, remoteClock, name, responseList) :
    # branch process selects the larger value from both the clocks and increments one
    self.clock = max(self.clock, remoteClock) + 1

    eventResponse = example_pb2.EventExecuted()
    eventResponse.id = self.id
    eventResponse.name = name
    eventResponse.clock = self.clock

    responseList.append(eventResponse)

# happens after all the propagate responses are returned from the branches
def Event_Response(self, name, responseList) :
    #The Branch process increments one from its local clock
    self.clock = self.clock + 1

    eventResponse = example_pb2.EventExecuted()
    eventResponse.id = self.id
    eventResponse.name = name
    eventResponse.clock = self.clock

    responseList.append(eventResponse)

# returns the balance in a branch 
def QueryInterface(self) :
    time.sleep(3)
    return self.balance

# deposits the money in the branch and propagates the update to fellow branches
def DepositInterface(self, event, remoteTime, responseList) :
    Event_Request(self, remoteTime, "deposit_request", responseList)
    Event_Execute(self, event, "deposit_execute", responseList)
    self.balance = self.balance + event.money
    result = Deposit_Propagate(self, event, responseList)
    Event_Response(self, "deposit_response", responseList)

    return result

# withdraws the amount from the branch and propagates the update to fellow branches
def WithdrawInterface(self, event, remoteTime, responseList) :
    Event_Request(self, remoteTime, "withdraw_request", responseList)
    Event_Execute(self, event, "withdraw_execute", responseList)
    if(self.balance >= event.money) : 
        self.balance = self.balance - event.money
        result = Withdraw_Propagate(self, event, responseList)
    else :
        result = 'Fail'
    Event_Response(self, "withdraw_response", responseList)

    return result

# increases the balance in the branches with the amount specified
def Deposit_Propagate(self, event, responseList) :
    for x in range(len(self.branches)) :
        if self.id != self.branches[x].id :
            Propagate_Request(self.branches[x], self.clock, "deposit_propagate_request", responseList)
            Propogate_Execute(self.branches[x], "deposit_propagate_execute", responseList)
            self.branches[x].balance = self.branches[x].balance + event.money
            Propogate_Response(self, self.branches[x].clock, "deposit_propagate_response", responseList)
    return 'success'
 
# decreases the balance in the branches with the amount specified
def Withdraw_Propagate(self, event, responseList) :
    for x in range(len(self.branches)) :
        if self.id != self.branches[x].id :
            Propagate_Request(self.branches[x], self.clock, "withdraw_propagate_request", responseList)
            Propogate_Execute(self.branches[x], "withdraw_propagate_execute", responseList)
            self.branches[x].balance = self.branches[x].balance - event.money
            Propogate_Response(self, self.branches[x].clock, "withdraw_propagate_response", responseList)
    return 'success'

# starts the server for each branch on specified port
def _run_server(bind_address, branch):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5),)
    example_pb2_grpc.add_RPCServicerServicer_to_server(branch, server)
    server.add_insecure_port(bind_address)
    server.start()
    server.wait_for_termination()
    
def main():

    # load branches data from JSON file
    with open('./input.json', 'r') as f:
        data = json.load(f)

    inputBankList = []
    for x in range(len(data)) :
        if data[x]['type'] == 'branch' :
            inputBankList.append(data[x])

    # create branch process for each input branch
    branchProcessesList = []
    for x in range(len(inputBankList)) :
        branch = Branch(inputBankList[x]['id'], inputBankList[x]['balance'], [])
        branchProcessesList.append(branch)

    # assign branch processes list to 'branches' parameter
    for x in range(len(branchProcessesList)) :
        branchProcessesList[x].branches = branchProcessesList

    # generate ports
    basicPort = 50051
    portList = []
    for x in range(len(branchProcessesList)) :
        port = basicPort + x
        portList.append(port)

    # creates process for each branch and starts the server
    workers = []
    for x in range(len(branchProcessesList)):
        bind_address = f"[::]:{portList[x]}"
        worker = multiprocessing.Process(target=_run_server, args=(bind_address, branchProcessesList[x]))
        worker.start()
        print(f'server started on port {portList[x]}')
        workers.append(worker)

    for worker in workers:
        worker.join()

if __name__ == "__main__":
    main()