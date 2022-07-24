import socket
import threading

HEADER = 64
PORT = 78
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
users = []  # Store user's name
sort = []  # Store user's socket


def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    print("[Starting] server is starting...")
    start(server)


def handle_client(conn, addr, server):
    print(f"[NEW CONNECTION] {addr} connected.")
    sort.append(conn)
    conn.send('Name'.encode(FORMAT))
    name = conn.recv(1024).decode(FORMAT)
    users.append(name)
    # conn.send('Welcome to the server'.encode(FORMAT))
    print(users)
    # print(sort)
    display_users(conn)
    send_everyone(server, conn, "SERVER", (f"{name} Joined!"))

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)

        if msg_length:

            # Disconnect User from the server.
            if msg == DISCONNECT_MESSAGE:
                print(f"[CONNECTION CLOSED] {addr} {name} disconnected")
                send_everyone(server, conn, "SERVER",
                              (f"{name} Disconnected!"))
                idx = sort.index(conn)
                sort.pop(idx)
                users.pop(idx)
                connected = False
                
                
                break

            print(f"[{name}] {msg}")

        send_everyone(server, conn, name, msg)

    conn.close()  # To close client socket connection.


def send_everyone(server, conn, name, msg):
    for i in sort:  # Send received messages to clients
        # Filter server and message sender. Send message except them.
        if(i != server and i != conn):
            i.sendall(f'[{name}] {msg}'.encode(FORMAT))


def display_users(conn):
    user_dis = '\n'.join(users)
    conn.send((f'[SERVER] Users in the chat:\n{user_dis}').encode(FORMAT))
   


def start(server):
    server.listen()
    print(f"[LISTENING] Server is running on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(
            target=handle_client, args=(conn, addr, server))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")


if __name__ == '__main__':
    main()
