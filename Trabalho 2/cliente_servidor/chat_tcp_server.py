import threading
import socket

clients: list[socket.socket] = []

def main(host: str, port: int):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((host, port))
        server.listen()
    except:
        return print("\nNão foi possível iniciar o servidor!\n")
    
    while True:
        client, addr = server.accept()
        
        clients.append(client)

        thread = threading.Thread(target=messages_treatment, args=[client])
        thread.start()


def messages_treatment(client: socket.socket):
    while True:
        try:
            msg = client.recv(1024)

            broadcast(msg, client)
        except:
            delete_client(client)
            break


def broadcast(msg: str, client: socket.socket):
    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(msg)
            except:
                delete_client(clientItem)


def delete_client(client: socket.socket):
    clients.remove(client)


if __name__ == "__main__":
    while not(host := input("HOST: ")): pass
    port = ""
    while not(port):
        try:
            port = int(input("PORT: "))
        except:
            print("Invalid PORT")
            port = ""

    main(host, port)