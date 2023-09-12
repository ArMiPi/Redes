import socket


BUFFER = 500    # 500, 1000 ou 1500
EXPECTED_PACKAGES = 100


def main(host: str, target_port: int):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    send_message(udp_socket, host, target_port)


def send_message(udp_socket: socket.socket, target_ip: str, target_port: int):
    """
    Manda "mensagens" com len() = BUFFER, sendo os últimos valores dessa "mensagem"
    o valor de i.

    Essas "mensagens" são enviadas para target_ip:target_port.
    """

    for i in range(1, EXPECTED_PACKAGES + 1):
        packet = f"{i}".zfill(BUFFER)

        udp_socket.sendto(packet.encode('utf-8'), (target_ip, target_port))

    udp_socket.close()
    

if __name__ == "__main__":
    host = '127.0.0.1'
    target_port = 7777
    
    main(host, target_port)
