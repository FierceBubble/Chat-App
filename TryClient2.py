import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

HEADER = 64
PORT = 78
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "202.186.211.250"
ADDR = (SERVER, PORT)
isCONNECTED = True


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Functions
def print_message(message):
    if isCONNECTED == True:
        message_box.config(state=tk.NORMAL)
        message_box.insert(tk.END, message + '\n')
        message_box.config(state=tk.DISABLED)


def join():
    # Connect to the server
    try:
        client.connect(ADDR)
        print("[SERVER] Successfully connected to the server!")
        print_message("[SERVER] Successfully connected to the server!")
    except ConnectionRefusedError:
        messagebox.showerror("Server connection error",
                             f"Unable to connect to server {SERVER}:{PORT}")
        print(f"Unable to connect to server {SERVER}:{PORT}")
        root.destroy()

    # If 'Name' received. It allows you to send the name.
    if ('Name' in client.recv(1024).decode(FORMAT)):
        name = username_textbox.get()  # Type name
        if name != '':
            join_button.pack_forget()
            disconnect_button.pack(side=tk.RIGHT, padx=10)

            client.send(name.encode(FORMAT))
            threading.Thread(
                target=listen_incoming_message_server).start()
        else:
            messagebox.showerror("Invalid Name", "Name cannot be empty!")
            print("Name cannot be empty!")
            root.destroy()

    username_textbox.config(state=tk.DISABLED)
    join_button.config(state=tk.DISABLED)


def listen_incoming_message_server():
    while 1:
        if isCONNECTED == True:
            # Receive messages from other clients.
            receive = client.recv(2048).decode(FORMAT)
            print(receive)
            print_message(receive)
        else:
            break


def send_message():
    msg = message_textbox.get()  # Enter message
    if msg != '':
        send(msg)
        message_textbox.delete(0, len(msg))
    elif (msg == DISCONNECT_MESSAGE):
        messagebox.showinfo("Disconnect Message", "You are disconnected!")
        print("You are disconnected!")


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def disconnect():
    root.destroy()

    send(DISCONNECT_MESSAGE)
    global isCONNECTED
    isCONNECTED = False


# Initiate GUI
root = tk.Tk()
# Width x height window size
root.geometry("600x600")
# Display name of the application
root.title("Appliaction Layer Programming Assignment")
# Width (NotResizeable) and Height (NotResizeable)
root.resizable(False, False)

# Colors and Fonts
DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = 'White'
FONT = ("Helventica", 17)
SMALL_FONT = ("Helventica", 13)
BUTTON_FONT = ("Helventica", 15)

# Creating the GUI
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

mid_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
mid_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

# Top Frame
username_label = tk.Label(
    top_frame, text="Enter Username:", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)
username_textbox = tk.Entry(
    top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)
join_button = tk.Button(
    top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=join)
join_button.pack(side=tk.RIGHT, padx=10)
disconnect_button = tk.Button(
    top_frame, text="Disconnect", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=disconnect)
disconnect_button.pack_forget()


# Middle Frame
message_box = scrolledtext.ScrolledText(
    mid_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

# Bottom Frame
message_textbox = tk.Entry(bottom_frame, font=FONT,
                           bg=MEDIUM_GREY, fg=WHITE, width=40)
message_textbox.pack(side=tk.LEFT, padx=10)
message_button = tk.Button(bottom_frame, text="Send",
                           font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.RIGHT, padx=10)


def main():
    root.mainloop()


if __name__ == '__main__':
    main()
