import socket
import threading

HEADER = 64
PORT = 78
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "202.186.211.250"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send_server():
    # If 'Name' received. It allows you to send the name.
    if('Name' in client.recv(1024).decode(FORMAT)):
        name = input('Enter Name : ')  # Type name
        client.send(name.encode(FORMAT))

    listen_thread = threading.Thread(target=listen_incoming_message_server)
    listen_thread.start()

    send_message()


def listen_incoming_message_server():

    while 1:
        # Receive messages from other clients.
        receive = client.recv(2048).decode(FORMAT)
        print(receive)


def send_message():

    while 1:
        data = input()  # Enter message
        send(data)

        if(data == DISCONNECT_MESSAGE):
            print("You are disconnected!")
            client.close()


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))
    client.send(send_length)
    client.send(message)


send_server()