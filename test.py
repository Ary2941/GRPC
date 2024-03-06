# server.py
import grpc
import threading
from concurrent import futures
from chat_pb2 import Message
from chat_pb2_grpc import ChatServiceServicer, add_ChatServiceServicer_to_server

class ChatServer(ChatServiceServicer):
    def __init__(self):
        self.clients = []
        self.lock = threading.Lock()

    def SendMessage(self, request, context):
        with self.lock:
            for client in self.clients:
                if client != context:
                    client.send(Message(sender=request.sender, content=request.content))
        return request

    def ReceiveMessage(self, request, context):
        with self.lock:
            self.clients.append(context)
        try:
            for message in context.__iter__():
                yield message
        finally:
            with self.lock:
                self.clients.remove(context)

    def SendDirectMessage(self, request, context):
        with self.lock:
            for client in self.clients:
                if client != context and client.peer() == request.content:
                    client.send(Message(sender=request.sender, content=request.content))
        return request

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_server = ChatServer()
    add_ChatServiceServicer_to_server(chat_server, server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Chat Server started on port 50051")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
