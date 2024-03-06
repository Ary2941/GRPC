import server
import client
import threading

destinatario = input("mandar mensagem para: ")
remetente = input("meu port: ")


threading.Thread(target=server.run_server,args=(destinatario,)).start()

client.Client(destinatario,remetente).run_client()


