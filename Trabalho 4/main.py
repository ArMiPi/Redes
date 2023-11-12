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

def format_scale(valor: float) -> str:
    """
    Retorna o valor fornecido convertido para uma string representando seu valor float
    com duas casas decimais e "reduzido" para G/M/K caso necessário
    """

    unidade = ""
    if valor >= 1_000_000_000:
        valor /= 1_000_000_000
        unidade = "G"
    elif valor >= 1_000_000:
        valor /= 1_000_000
        unidade = "M"
    elif valor >= 1_000:
        valor /= 1_000
        unidade = "K"
    else:
        pass

    return f"{locale.format_string('%.2f', valor, grouping=True)} {unidade}"
        

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
            execution_time = time.perf_counter()
            tam_pacotes_recebidos = conexao.recieve_message()
            execution_time = time.perf_counter() - execution_time
            if protocolo == "-udp":
                execution_time -= TIME_OUT
            time.sleep(1)

            # Receber quantidade de pacotes enviados
            conexao = TCP(modo)
            tam_pacotes_enviados = int(conexao.client.recv(BUFFER).decode('utf-8'))
        case _:
            print("Modo inválido [u/d]")
            exit()

    if modo == "-d":
        pacotes_enviados = tam_pacotes_enviados / BUFFER
        pacotes_recebidos = tam_pacotes_recebidos / BUFFER
        perda_de_pacotes = pacotes_enviados - pacotes_recebidos

        velocidade_bit_seg_upload = tam_pacotes_enviados * 8 / execution_time
        velocidade_bit_seg_download = tam_pacotes_recebidos * 8 / execution_time

        velocidade_pacotes_seg_upload = pacotes_enviados / execution_time
        velocidade_pacotes_seg_download = pacotes_recebidos / execution_time

        print(f"""
            =============================================================
                Pacotes Enviados:  {locale.format_string('%.0f', pacotes_enviados, grouping=True)} pacotes
                Pacotes Recebidos: {locale.format_string('%.0f', pacotes_recebidos, grouping=True)} pacotes
                Perda de Pacotes:  {locale.format_string('%.0f', perda_de_pacotes, grouping=True)} pacotes perdidos
            =============================================================
                Bytes enviados:  {locale.format_string('%.0f', tam_pacotes_enviados, grouping=True)} bytes
                Bytes recebidos: {locale.format_string('%.0f', tam_pacotes_recebidos, grouping=True)} bytes
                Perda de Bytes:  {locale.format_string('%.0f', tam_pacotes_enviados - tam_pacotes_recebidos, grouping=True)} bytes
            =============================================================
                Velocidade de upload: 
                    {format_scale(velocidade_bit_seg_upload)}bit/s
                    {locale.format_string('%.2f', velocidade_pacotes_seg_upload, grouping=True)} pacotes/s
                Velocidade de download:
                    {format_scale(velocidade_bit_seg_download)}bit/s
                    {locale.format_string('%.2f', velocidade_pacotes_seg_download, grouping=True)} pacotes/s
        """)
