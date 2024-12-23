from socket import *
import threading
from tkinter import *
from tkinter import simpledialog
import datetime  

class Chat:
    def __init__(self):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.connect(('192.168.1.104', 444))
        login = Tk()
        login.withdraw()
        self.janela_carregada = False
        self.ativo = True
        self.nome = simpledialog.askstring('Nome', 'Digite o seu nome|', parent=login)
        self.sala = simpledialog.askstring('Sala', 'Digite a sala que deseja entrar|', parent=login)
        self.janela()

    def janela(self):
        self.root = Tk()
        self.root.geometry("800x800")
        self.root.title('Chat')
        self.caixa_texto = Text(self.root)
        self.caixa_texto.place(relx=0.05, rely=0.01, width=700, height=600)
        self.envia_mensagem = Entry(self.root)
        self.envia_mensagem.place(relx=0.05, rely=0.8, width=500, height=20)
        self.btn_enviar = Button(self.root, text="Enviar", command=self.enviarMensagem)
        self.btn_enviar.place(relx=0.7, rely=0.8, width=100, height=20)
        self.root.protocol('WM_DELETE_WINDOW', self.fechar)
        thread = threading.Thread(target=self.conecta)
        thread.daemon = True  
        thread.start()
        self.root.mainloop()

    def fechar(self):
        self.ativo = False
        self.root.quit()
        self.client.close()

    def conecta(self):
        while self.ativo:
            try:
                recebido = self.client.recv(1024)
                if recebido == b'SALA':
                    self.client.send(self.sala.encode())
                    self.client.send(self.nome.encode())
                else:
                    try:
                        self.caixa_texto.insert('end', recebido.decode())
                    except:
                        pass
            except Exception as e:
                print("Erro ao receber mensagem:", e)
                break

    def enviarMensagem(self):
        mensagem = self.envia_mensagem.get()
        hora_atual = datetime.datetime.now().strftime('%H:%M:%S')
        data_atual = datetime.datetime.now().strftime('%Y-%m-%d')  
        mensagem_com_hora = f'[{data_atual}] {self.nome}: {mensagem} |[{hora_atual}]|'  
        self.client.send(mensagem_com_hora.encode())
        self.envia_mensagem.delete(0, END)

chat = Chat()
