import threading
import socket


def main(host: str, port: int):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((host, port))
    except:
        return print("\nNão foi possível se conectar ao servidor!\n")

    username = input('Usuário: ')
    print('\nConectado')

    thread1 = threading.Thread(target=recieve_messages, args=[client])
    thread2 = threading.Thread(target=send_messages, args=[client, username])

    thread1.start()
    thread2.start()


def recieve_messages(client: socket.socket):
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            print(f"{msg}\n")
        except:
            print('\nConexão com o servidor foi perdida!\n')
            print('Pressione <Enter> para continuar...')
            
            client.close()

            break


def send_messages(client: socket.socket, username: str):
    while True:
        try:
            msg = input('\n')
            client.send(f'<{username}> {msg}'.encode('utf-8'))
        except:
            return


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