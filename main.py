# python -m grpc_tools.protoc -Isrc --python_out=src --grpc_python_out=src src/source.proto

import grpc

import src.source_pb2 as chat
import src.source_pb2_grpc as rpc
import threading

from concurrent import futures
import time

channel = grpc.insecure_channel('localhost:2491')

stub = rpc.chatStub(channel)

class services(rpc.chatServicer):
    def __init__(self):
        ultima_carta = None
        pass

    def receberCarta(self, request, context):
        print("receberCarta",self.ultima_carta)

    def remeterCarta(self, request: chat.Carta, context):
        print(f"{request.nome}:{request.mensagem}")

        return chat.Nada()
    
    def remeterRelogio(self, request: chat.Relogio, context):
        print(f"!{request.time}")

        return chat.Nada()


def run_server(port):

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_chatServicer_to_server(services(), server)

    try:
        server.add_insecure_port('[::]:' + str(port))
        print(f'Starting server. Listening at {port}...')

        server.start()

        server.wait_for_termination()
    except Exception as e:
        # Ignorar exceções específicas que você quer evitar
        print("OPS:", e)

run_server("2491")