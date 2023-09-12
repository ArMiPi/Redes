from threading import Thread
import socket

def main(host: str, port: int):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Tenta realizar um bind na porta especificada
    # Caso consiga, fica esperando uma conexão
    try:
        client.bind((host, port))
        client.listen()
    except:
        return print("\nNão foi possível conectar ao servidor\n")
    
    # Aceita uma conexão
    clt, addr = client.accept()
    # Inicia as threads para receber e enviar mensagens
    thread1 = Thread(target=recieve_message, args=[clt])
    thread2 = Thread(target=send_message, args=[clt])
    thread1.start()
    thread2.start()
    thread1.join()


def recieve_message(client: socket.socket):
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')

            print(f">> {msg}")
        except:
            client.close()
            return


def send_message(cliente: socket.socket):
    while True:
        try:
            msg = input('\n')
            cliente.send(msg.encode('utf-8'))
        except:
            return


if __name__ == "__main__":
    while not(host := input("HOST: ")): pass
    
    port = ""
    while not port:
        try:
            port = int(input("PORT: "))
        except:
            print("\nINVALID PORT\n")
            port = ""

        
    main(host, port)

