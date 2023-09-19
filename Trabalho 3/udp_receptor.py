import locale
import socket
import time
import hashlib
from fpdf import FPDF

from env_config import BUFFER, HEADER_SIZE, CHECK_SUM_SIZE, HOST, PORT, TCP_PORT, TCP_HOST

TIME_OUT = 10


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def main(host: str, port: int) -> tuple[list[str], int, float]:
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.settimeout(TIME_OUT)

    # Tenta conectar com a aplicação em host:port
    try:
        udp_socket.bind((host, port))
    except:
        return print("\nNão foi possível conectar ao servidor\n")
    
    start_time = time.perf_counter()
    received_data, tamanho_total_dados = recieve_message(udp_socket)
    end_time = time.perf_counter()

    execution_time = end_time - start_time - TIME_OUT

    udp_socket.close()

    return received_data, tamanho_total_dados, execution_time


def recieve_message(udp_socket: socket.socket) -> tuple[list[str], int]:
    received_data = []
    tamanho_total_dados = 0

    while(True):
        try:
            packet, _ = udp_socket.recvfrom(BUFFER)

            packet = packet.decode('utf-8')

            header = packet[ : HEADER_SIZE]
            body = packet[HEADER_SIZE : BUFFER - CHECK_SUM_SIZE]
            check_sum = packet[BUFFER - CHECK_SUM_SIZE : ]

            sha256 = hashlib.sha256()
            sha256.update(f"{header}{body}".encode())
            check = sha256.hexdigest()
            check = check[-CHECK_SUM_SIZE : ]

            if(check == check_sum):
                received_data.append(packet)
            else:
                print("Pacote corrompido")
            
            tamanho_total_dados += len(packet)

        except socket.timeout:
            print("TIMEOUT :)")
            break
        
    return received_data, tamanho_total_dados


def create_pdf(tamanho_total_dados: int, expected_packages: int, received_data: int, execution_time: float):
    pdf = FPDF()

    pdf.add_page()
    pdf.set_font("Arial", size=15)

    pdf.cell(200, 10, txt="="*50, align='C', ln=1)
    pdf.cell(200, 10, txt=f"{'Relatório':^50}", align='C', ln=2)
    pdf.cell(200, 10, txt="="*50, align='C', ln=3)
    pdf.cell(200, 10, txt=f"Tamanho do arquivo: {locale.format_string('%.0f', tamanho_total_dados, grouping=True)} bytes", align='C', ln=4)
    pdf.cell(200, 10, txt=f"Número de pacores enviados: {expected_packages}", align='C', ln=5)
    pdf.cell(200, 10, txt=f"Número de arquivos recebidos: {received_data}", align='C', ln=6)
    pdf.cell(200, 10, txt=f"Número de arquivos perdidos: {expected_packages - received_data}", align='C', ln=7)
    pdf.cell(200, 10, txt=f"Velocidade de transmissão: {locale.format_string('%.4f', tamanho_total_dados * 8 / execution_time, grouping=True)} bit/s", align='C', ln=8)
    pdf.cell(200, 10, txt="="*50, align='C', ln=9)

    pdf.output("relatorio.pdf")


if __name__ == "__main__":
    host = HOST
    target_port = PORT
    tcp_port = TCP_PORT
    tcp_host = TCP_HOST

    received_data, tamanho_total_dados, execution_time = main(host, target_port)


    # RECEBER QUANTIDADE ESPERADA DE PACOTES VIA TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((tcp_host, tcp_port))
    expected_packages = int(client.recv(BUFFER).decode('utf-8'))

    # Apresentar um relatório na tela e em pdf com:
    #   - Tamanho do arquivo transmitido
    #   - Número de pacotes enviados, recebidos e perdidos
    #   - Velocidade de transmissão em bit/s
    print("="*50)
    print(f"{'Relatório':^50}")
    print("="*50)
    print(f"Tamanho do arquivo: {locale.format_string('%.0f', tamanho_total_dados, grouping=True)} bytes")
    print(f"Número de pacores enviados: {expected_packages}")
    print(f"Número de arquivos recebidos: {len(received_data)}")
    print(f"Número de arquivos perdidos: {expected_packages - len(received_data)}")
    print(f"Velocidade de transmissão: {locale.format_string('%.4f', tamanho_total_dados * 8 / execution_time, grouping=True)} bit/s")
    print("="*50)

    create_pdf(tamanho_total_dados, expected_packages, len(received_data), execution_time)
