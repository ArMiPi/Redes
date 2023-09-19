import socket
import hashlib

from env_config import BUFFER, HEADER_SIZE, CHECK_SUM_SIZE, HOST, PORT, TCP_PORT, TCP_HOST

BODY_SIZE = BUFFER - HEADER_SIZE - CHECK_SUM_SIZE


def main(host: str, target_port: int) -> int:
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    packages = send_message(udp_socket, host, target_port)

    return packages


def send_message(udp_socket: socket.socket, target_ip: str, target_port: int) -> int:
    """
    Manda "mensagens" com len() = BUFFER, sendo os últimos valores dessa "mensagem"
    o valor de i.

    Essas "mensagens" são enviadas para target_ip:target_port.

    Retorna o número de pacotes enviados
    """

    # Armazenar a mensagem
    msg = ""
    with open("message.txt", "r") as file:
        msg = file.read()

    pack_num = 0
    while(True):
        # Montar o HEADER do pacote
        header = f'{pack_num+1}'.zfill(HEADER_SIZE)

        # Montar o BODY do pacote
        start = pack_num * BODY_SIZE

        if start >= len(msg):
            break

        if start + BODY_SIZE > len(msg):
            body = msg[start : ]
            body = f"{body}{'$'*(BODY_SIZE - len(body))}"
        else:
            body = msg[start : start+BODY_SIZE]
        
        # Montar o CHECK SUM do pacote
        sha256 = hashlib.sha256()
        sha256.update(f"{header}{body}".encode())
        check_sum = sha256.hexdigest()
        check_sum = check_sum[-CHECK_SUM_SIZE : ]

        # Montar o pacote
        packet = f"{header}{body}{check_sum}"
        
        # Enviar o pacote
        udp_socket.sendto(packet.encode('utf-8'), (target_ip, target_port))

        pack_num += 1

    udp_socket.close()

    return pack_num

    

if __name__ == "__main__":
    host = HOST
    target_port = PORT
    tcp_port = TCP_PORT
    tcp_host = TCP_HOST
    
    packages = main(host, target_port)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.bind((tcp_host, tcp_port))
    client.listen()
    client, _ = client.accept()

    client.send(f'{packages}'.encode('utf-8'))
    client.close()
