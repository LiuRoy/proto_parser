from __future__ import print_function

import grpc

import helloworld_pb2
import helloworld_pb2_grpc

from protoparser import make_client


def run1():
    channel = grpc.insecure_channel('localhost:50051')
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(helloworld_pb2.HelloRequest(name='abc'))
    print("Greeter client received: " + response.name)


def run2():
    client = make_client('./helloworld.proto')
    channel = grpc.insecure_channel('localhost:50051')
    stub = client.GreeterStub(channel)
    response = stub.SayHello(client.HelloRequest(name='abc'))
    print("Greeter client received: " + response.name)


if __name__ == '__main__':
    run2()