# python -m grpc_tools.protoc -Isrc --python_out=src --grpc_python_out=src src/source.proto

import grpc

import src.source_pb2 as chat
import src.source_pb2_grpc as rpc
import threading

from concurrent import futures
import time

start = time.time()

class services(rpc.chatServicer):
    def __init__(self):
        self.mensagens = [chat.Carta(nome="server",mensagem="mensagem 1"),chat.Carta(nome="server",mensagem="mensagem 2")]
        pass

    def receberCarta(self, request, context):
        for mensagem in self.mensagens:
            yield mensagem 

    def remeterCarta(self, request: chat.Carta, context):
        print(f"{request.nome}:{request.mensagem}")

        return chat.Nada()
    
    def remeterRelogio(self, request: chat.Relogio, context):
        print(f"clock from {request.nome}: {request.time}")

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

run_server("12")