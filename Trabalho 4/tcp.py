from typing import Literal
from typing_extensions import Self
from env_config import BUFFER, TIMER, IP_UPLOAD, IP_DOWNLOAD, PORT
import socket
import time

class TCP:
    def __init__(self: Self, modo: Literal["-d", "-u"]) -> None:
        self.client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if modo == "-d":
            try:
                self.client.connect((IP_DOWNLOAD, PORT))
            except Exception as e:
                print(e)
                return print("\nNão foi possível conectar ao servidor\n")
        elif modo == "-u":
            try:
                self.client.bind((IP_UPLOAD, PORT))
                self.client.listen()

                self.client, _ = self.client.accept()
            except Exception as e:
                print(e)
                return print("\nNão foi possível criar a conexão\n")


    def send_message(self: Self, message: str) -> int:
        """
        Envia a mensagem informada durante um tempo pré definido e retorna a quantidade
        de pacotes enviada
        """
        timeout = time.time() + TIMER
        pacotes = 0

        while True:
            try:
                if time.time() > timeout: 
                    raise TimeoutError
                
                self.client.send(message.encode('utf-8'))
                pacotes += len(message)
            
            except TimeoutError as _:
                print("TCP send_message: TIMEOUT :)")
                self.client.close()
                return pacotes
            except Exception as e:
                print(f"[ERROR] TCP send_message: {e}")
                self.client.close()
                return pacotes


    def recieve_message(self: Self) -> int:
        """
        Recebe as mensagens enviadas e retorna a quantidade recebida
        """
        pacotes = 0

        while True:
            try:
                msg = self.client.recv(BUFFER).decode('utf-8')
                if msg:
                    pacotes += len(msg)
            except Exception as _:
                self.client.close()
                return pacotes


