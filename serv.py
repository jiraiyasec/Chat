from socket import *
import threading
red = "\033[31m"
yellow = "\033[33m"
green = "\033[32m"
reset = "\033[0m"
blue = "\033[34m"
server = socket(AF_INET, SOCK_STREAM)
server.bind(('192.168.1.104', 444))
server.listen()
salas = {}

def broadcast(sala, mensagem):
    for client in salas[sala]:
        if isinstance(mensagem, str):
            mensagem = mensagem.encode()
        try:
            client.send(mensagem)
        except:
            salas[sala].remove(client)

def enviarMensagem(nome, sala, client):
    while True:
        try:
            mensagem = client.recv(1024)
            if not mensagem:
                break
            mensagem = f'{nome}:|{mensagem.decode()}|\n'
            broadcast(sala, mensagem)
        except Exception as e:
            print(f"Erro ao enviar mensagem de {nome}: {e}")
            break
    client.close()
    salas[sala].remove(client)
    broadcast(sala, f'{nome} saiu da sala\n')

while True:
    client, addr = server.accept()
    client.send(b'SALA')
    sala = client.recv(1024).decode()
    nome = client.recv(1024).decode()
    if sala not in salas.keys():
        salas[sala] = []
    salas[sala].append(client)
    print(f'[{yellow}{reset}{green}{nome} se conectou na sala{reset}{yellow} {sala}{reset} {blue}ip{reset} {red}{addr[0]}{reset}')
    broadcast(sala, f'{nome} entrou na sala\n')
    thread = threading.Thread(target=enviarMensagem, args=(nome, sala, client))
    thread.daemon = True 
    thread.start()
