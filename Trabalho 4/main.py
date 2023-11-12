from env_config import BUFFER
import sys
import locale
import time

from tcp import TCP
from udp import UDP, TIME_OUT

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

    # Protocolo e modo utilizados
    protocolo = args[1]
    modo = args[2]

    # Tempo de execução
    execution_time = 0

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
            execution_time = time.perf_counter()
            tam_pacotes_enviados = int(conexao.client.recv(BUFFER).decode('utf-8'))
            execution_time = time.perf_counter() - execution_time - TIME_OUT
        case _:
            print("Modo inválido [u/d]")
            exit()

    if modo == "-d":
        pacotes_enviados = tam_pacotes_enviados / BUFFER
        pacotes_recebidos = tam_pacotes_recebidos / BUFFER
        velocidade_bit_seg_upload = tam_pacotes_enviados / execution_time
        velocidade_pacotes_seg_upload = pacotes_enviados / execution_time
        velocidade_bit_seg_download = tam_pacotes_recebidos / execution_time
        velocidade_pacotes_seg_download = pacotes_recebidos / execution_time
        perda_de_pacotes = pacotes_enviados - pacotes_recebidos

        print(f"""
            =============================================================
            Pacotes Enviados: {pacotes_enviados} pacotes
            Pacotes Recebidos: {pacotes_recebidos} pacotes
            Perda de Pacotes: {perda_de_pacotes} pacotes perdidos
            =============================================================
            Bytes enviados: {tam_pacotes_enviados} bytes
            Bytes recebidos: {tam_pacotes_recebidos} bytes
            Perda de Bytes: {tam_pacotes_enviados - tam_pacotes_recebidos} bytes
            =============================================================
            Velocidade de upload: 
                {velocidade_bit_seg_upload} bit/s
                {velocidade_pacotes_seg_upload} pacotes/s
            Velocidade de download:
                {velocidade_bit_seg_download} bit/s
                {velocidade_pacotes_seg_download} pacotes/s
        """)
