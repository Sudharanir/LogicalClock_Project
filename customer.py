import multiprocessing
import json
import os
import pprint

import grpc
import example_pb2_grpc
import example_pb2

class Customer:
    def __init__(self, id, events):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = events
        # pointer for the stub
        self.stub = None
        # the local clock of the customer
        self.clock = 1
    
    # function to create stub for customers
    def createStub(self):
        server_address = "localhost:50051"
        channel = grpc.insecure_channel(
            server_address,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
                ("grpc.so_reuseport", 1),
                ("grpc.use_local_subchannel_pool", 1),
            ],
        )
        stub = example_pb2_grpc.RPCServicerStub(channel)
        self.stub = stub

    # function to send out the events to the Bank branch
    def executeEvents(self):
        request = example_pb2.Request(id = self.id, events = self.events, clock = self.clock )
        self.clock = self.clock + 1
        response = self.stub.MsgDelivery(request)
        return response

# function to create customer process and perform the respective tasks
def _run_worker_query(customerInput) :
    customerProcess = Customer(customerInput['id'], customerInput['events'])
    customerProcess.createStub()
    response = customerProcess.executeEvents()
    return response

def run() :
    # load customers data from JSON file
    with open('./input.json', 'r') as f:
        data = json.load(f)

    customersInputList = []
    for x in range(len(data)) :
        if data[x]['type'] == 'customer' :
            customersInputList.append(data[x])

    worker_pool = multiprocessing.Pool(processes=len(customersInputList),)
    response = worker_pool.map(_run_worker_query, customersInputList)

    # generating output format and displaying in the console
    responseList = []
    for x in range(len(customersInputList)) :
        branchDict = {
            'pid' : x+1,
            'data' : []
        }
        responseList.append(branchDict)

    for x in range(len(response)) :
        if(len(response[x].data) > 0) :
            for y in range(len(response[x].data)) :
                eventDict = {}
                eventDict['id'] = response[x].id
                eventDict['name'] = response[x].data[y].name
                eventDict['clock'] = response[x].data[y].clock

                branchId = response[x].data[y].id
                temp = responseList[branchId-1]['data']
                if(len(temp) == 0) :
                    temp.append(eventDict)
                else :
                    for k in range(len(temp)) :
                        if(temp[k]['clock'] <= eventDict['clock']) :
                            if(k==len(temp)-1) :
                                temp.append(eventDict)
                            else :
                                continue
                        elif(temp[k]['clock'] > eventDict['clock']) :
                            temp.insert(k, eventDict)
                            break
                        else :
                            temp.append(eventDict)
                            break

    for x in range(len(response)) :
        responseDict = {}
        if(len(response[x].data) > 0) :
            responseDict['eventid'] = response[x].id
            tempList = []
            for y in range(len(response[x].data)) :
                recvDict = {}
                recvDict['clock'] = response[x].data[y].clock
                recvDict['name'] = response[x].data[y].name
                tempList.append(recvDict)
            responseDict['data'] = tempList
            responseList.append(responseDict)

    pprint.pprint(responseList, sort_dicts=False)

if __name__ == "__main__":
    run()