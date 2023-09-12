import socket
import hashlib

from env_config import BUFFER, HEADER_SIZE, CHECK_SUM_SIZE, HOST, PORT

PACKAGES = 100


def main(host: str, target_port: int):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    send_message(udp_socket, host, target_port)


def send_message(udp_socket: socket.socket, target_ip: str, target_port: int):
    """
    Manda "mensagens" com len() = BUFFER, sendo os últimos valores dessa "mensagem"
    o valor de i.

    Essas "mensagens" são enviadas para target_ip:target_port.
    """

    for i in range(1, PACKAGES + 1):
        header = f'{i}'.zfill(HEADER_SIZE)
        body = f"{i}".zfill(BUFFER - HEADER_SIZE - CHECK_SUM_SIZE)
        
        sha256 = hashlib.sha256()
        sha256.update(f"{header}{body}".encode())
        check_sum = sha256.hexdigest()
        check_sum = check_sum[-CHECK_SUM_SIZE :]

        packet = f"{header}{body}{check_sum}"

        udp_socket.sendto(packet.encode('utf-8'), (target_ip, target_port))

    udp_socket.close()
    

if __name__ == "__main__":
    host = HOST
    target_port = PORT
    
    main(host, target_port)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.bind((host, target_port))
    client.listen()
    client, _ = client.accept()

    client.send(f'{PACKAGES}'.encode('utf-8'))
    client.close()
