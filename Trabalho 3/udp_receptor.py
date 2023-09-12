import locale
import socket
import time

from udp_emissor import BUFFER, EXPECTED_PACKAGES


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def main(host: str, port: int) -> tuple[list[str], int, float]:
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.settimeout(5)    # 3s para timeout

    # Tenta conectar com a aplicação em host:port
    try:
        udp_socket.bind((host, port))
    except:
        return print("\nNão foi possível conectar ao servidor\n")
    
    start_time = time.perf_counter()
    received_data, tamanho_total_dados = recieve_message(udp_socket)
    end_time = time.perf_counter()

    execution_time = end_time - start_time - 5

    udp_socket.close()

    return received_data, tamanho_total_dados, execution_time


def recieve_message(udp_socket: socket.socket) -> tuple[list[str], int]:
    received_data = []
    tamanho_total_dados = 0

    while(True):
        try:
            packet, _ = udp_socket.recvfrom(BUFFER)

            packet = packet.decode('utf-8')

            received_data.append(packet)
            
            tamanho_total_dados += len(packet)


        except socket.timeout:
            print("TIMEOUT :)")
            break
        
    return received_data, tamanho_total_dados


if __name__ == "__main__":
    host = '127.0.0.1'
    target_port = 7777

    received_data, tamanho_total_dados, execution_time = main(host, target_port)

    # Apresentar um relatório na tela e em pdf com:
    #   - Tamanho do arquivo transmitido
    #   - Número de pacotes enviados, recebidos e perdidos
    #   - Velocidade de transmissão em bit/s
    print("="*50)
    print(f"{'Relatório':^50}")
    print("="*50)
    print(f"Tamanho do arquivo: {locale.format_string('%.0f', tamanho_total_dados, grouping=True)} bytes")
    print(f"Número de pacores enviados: {EXPECTED_PACKAGES}")
    print(f"Número de arquivos recebidos: {len(received_data)}")
    print(f"Número de arquivos perdidos: {EXPECTED_PACKAGES - len(received_data)}")
    print(f"Velocidade de transmissão: {locale.format_string('%.4f', tamanho_total_dados * 8 / execution_time, grouping=True)} bit/s")
    print("="*50)
