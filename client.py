import grpc

import src.source_pb2 as chat
import src.source_pb2_grpc as rpc

import threading

import time

start = time.time()


class Client:

    def __init__(self,port, u="cliente"):
        self.username = u
        self.conectado = False
        self.conectar(port)

    def conectar(self,port):
        while not self.conectado:
            try:
                print("connbecting...")
                channel = grpc.insecure_channel('localhost:' + str(port))
                self.stub = rpc.chatStub(channel)
                try:
                    self.stub.remeterCarta(chat.Carta(nome=self.username,mensagem="hello!"))
                    self.conectado = True
                except:
                    raise grpc.RpcError

            except grpc.RpcError as e:
                print("Erro ao acessar servidor:", e)
                self.conectado = False

    def mandar_carta(self, message):
        if message != '':
            lettre = chat.Carta(nome=self.username,mensagem=message)
            self.stub.remeterCarta(lettre)


    def mandar_relogio(self, tempo):
        if tempo != 0 and self.conectado:
            clock = chat.Relogio()
            clock.nome = self.username
            clock.time = tempo
            self.stub.remeterRelogio(clock)

    def receber_carta(self):
        for response in self.stub.receberCarta(chat.Nada()):
            print(f"carta: {response.nome} {response.mensagem}")
    
    def mandando_cartas(self):
        while 1:
            if self.conectado:
                message = input("")
                self.mandar_carta(message)


    def run_client(self):
        self.mandar_relogio(start)
        self.receber_carta()

        threading.Thread(target=self.mandando_cartas).start()


Client(input("mandar mensagem para: "),input("meu port: ")).run_client()