from env_config import BUFFER
import sys
import locale
import time

from tcp import TCP
from udp import UDP

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def create_message() -> str:
    """
    Cria a mensagem que será enviada
    """
    
    string = "teste de rede *2023*"

    string_final = string*(BUFFER//len(string))
    string_final += string[:(BUFFER - len(string_final))]

    return string_final

if __name__ == "__main__":
    args = sys.argv

    # Mensagem a ser enviada
    message = create_message()

    protocolo = args[1]
    modo = args[2]

    # Estabelecer protocolo TCP ou UDP
    conexao = None
    match protocolo:
        case "-tcp":
            conexao = TCP(modo)
        case "-udp":
            conexao = UDP(modo)
        case _:
            print("Protocolo inválido [udp/tcp]")
            exit()

    # Modo: -u = Upload e -d = Download
    match modo:
        case "-u":
            # Enviar pacotes
            tam_pacotes_enviados = conexao.send_message(message)
            time.sleep(1)

            # Enviar quantidade de pacotes enviados
            conexao = TCP(modo)
            conexao.client.send(f'{tam_pacotes_enviados}'.encode('utf-8'))
            conexao.client.close()
            exit()
        case "-d":
            # Receber pacotes
            tam_pacotes_recebidos = conexao.recieve_message()
            time.sleep(1)

            # Receber quantidade de pacotes enviados
            conexao = TCP(modo)
            tam_pacotes_enviados = int(conexao.client.recv(BUFFER).decode('utf-8'))
        case _:
            print("Modo inválido [u/d]")
            exit()

    # TODO Apresentar resultados

