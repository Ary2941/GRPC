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
                channel = grpc.insecure_channel('localhost:' + str(port))
                self.conn = rpc.chatStub(channel)
                self.conectado = True

            except grpc.RpcError as e:
                print("Erro ao acessar servidor:", e)
                self.conectado = False

    def mandar_carta(self, message):
        if message != '' and self.conectado:
            lettre = chat.Carta()
            lettre.nome = self.username
            lettre.mensagem = message
            self.conn.remeterCarta(lettre)

    def mandar_relogio(self, tempo):
        if tempo != 0 and self.conectado:
            clock = chat.Relogio()
            clock.nome = self.username
            clock.time = tempo
            self.conn.remeterRelogio(clock)

    def mandando_cartas(self):
        while 1:
            if self.conectado:
                message = input("")
                self.mandar_carta(message)
                now = time.time()-start
                self.mandar_relogio(now)


    def run_client(self):
        threading.Thread(target=self.mandando_cartas).start()

Client(input("mandar mensagem para: "),input("meu port: ")).run_client()