from typing import Literal
from typing_extensions import Self
from env_config import BUFFER, TIMER, IP_UPLOAD, PORT
import socket
import time

TIME_OUT = 10

class UDP:
    def __init__(self, modo: Literal["-d", "-u"]) -> None:
        self.client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if modo == "-d":
            try:
                self.client.bind((IP_UPLOAD, PORT))
                self.client.settimeout(TIME_OUT)
            except Exception as e:
                print(e)
                return print('\nNão foi possível conectar ao servidor\n')
        elif modo == "-u":
            pass


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
                self.client.sendto(message.encode('utf-8'), (IP_UPLOAD, PORT))
                pacotes += len(message)
            except TimeoutError as _:
                print("TIMEOUT :)")
                self.client.close()
                return pacotes
            except Exception as e:
                print(f"[ERROR] UDP send_message: {e}")
                self.client.close()
                return pacotes


    def recieve_message(self: Self) -> int:
        """
        Recebe as mensagens enviadas e retorna a quantidade recebida
        """
        pacotes = 0
        while True:
            try:
                msg, _ = self.client.recvfrom(BUFFER)
                msg = msg.decode('utf-8')

                if msg:
                    pacotes += len(msg)
            except socket.timeout:
                print("TIMEOUT :)")
                self.client.close()
                return pacotes
            except Exception as e:
                print(e)
                self.client.close()
                return pacotes