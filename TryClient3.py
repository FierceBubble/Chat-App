import socket
import threading
import tkinter as tk
from tkinter import END, scrolledtext
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
def print_message(message, sender):
    if isCONNECTED == True:
        message_box.config(state=tk.NORMAL)
        message_box.tag_configure("Server", foreground="Yellow", justify='left')
        message_box.tag_configure("Me", background=LIGHT_GREEN ,foreground=PASTEL_AQUA, justify='right')
        message_box.tag_configure("Others", background=MEDIUM_GREEN, foreground="Black", justify='left')
        message_box.insert(tk.END, message + '\n', sender)
        message_box.yview(END)
        message_box.config(state=tk.DISABLED)


def join(self):
    # Connect to the server
    try:
        client.connect(ADDR)
        print("[SERVER] Successfully connected to the server!")
        print_message("[SERVER] Successfully connected to the server!", "Server")
    except ConnectionRefusedError:
        messagebox.showerror("Server connection error",
                             f"Unable to connect to server {SERVER}:{PORT}")
        print(f"Unable to connect to server {SERVER}:{PORT}")
        root.destroy()

    # If 'Name' received. It allows you to send the name.
    if ('Name' in client.recv(1024).decode(FORMAT)):
        global name
        name = username_textbox.get()  # Type name
        if name != '':
            username_label.config(text=(f"Welcome to the server, {name}!"))
            username_textbox.pack_forget()
            join_button.config(text="DISCONNECT", command=disconnect)

            client.send(name.encode(FORMAT))
            threading.Thread(
                target=listen_incoming_message_server).start()
            
        else:
            messagebox.showerror("Invalid Name", "Name cannot be empty!")
            print("Name cannot be empty!")
            root.destroy()

    
            
def listen_incoming_message_server():
    while 1:
        if isCONNECTED == True:
            # Receive messages from other clients.
            receive = client.recv(2048).decode(FORMAT)
            print(receive)
            if receive[:8] == "[SERVER]":
                print_message(receive, "Server")
            else:
                print_message(receive, "Others")
        else:
            break
        
            
def send_message(self):
    msg = message_textbox.get()  # Enter message
    if msg != '':
        send(msg)
        print_message((f"{msg}"), "Me")
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
DARK_GREEN = '#94B49F'
MEDIUM_GREEN = '#B4CFB0'
LIGHT_GREEN = '#E5E3C9'
PASTEL_AQUA = '#789395'
WHITE = 'White'
FONT = ("Helventica", 17)
SMALL_FONT = ("Helventica", 13)
BUTTON_FONT = ("Helventica", 15)

# Creating the GUI
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=MEDIUM_GREEN)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

mid_frame = tk.Frame(root, width=200, height=400, bg=MEDIUM_GREEN)
mid_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=MEDIUM_GREEN)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

# Top Frame
username_label = tk.Label(
    top_frame, text="Enter Name:", font=FONT, bg=MEDIUM_GREEN, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)
username_textbox = tk.Entry(
    top_frame, font=FONT, bg=LIGHT_GREEN, fg=PASTEL_AQUA, width=23)
username_textbox.pack(side=tk.LEFT)
username_textbox.bind('<Return>', join)
join_button = tk.Button(
    top_frame, text="Join", font=BUTTON_FONT, bg=PASTEL_AQUA, fg=WHITE, command=lambda: join(None))
join_button.pack(side=tk.RIGHT, padx=30)


# Middle Frame
message_box = scrolledtext.ScrolledText(
    mid_frame, font=SMALL_FONT, bg=DARK_GREEN, fg=WHITE, width=62, height=26.5)
message_box.config(state=tk.DISABLED, padx=2)
message_box.pack(side=tk.TOP)

# Bottom Frame
message_textbox = tk.Entry(bottom_frame, font=FONT,
                           bg=LIGHT_GREEN, fg=PASTEL_AQUA, width=36)
message_textbox.pack(side=tk.LEFT, padx=10)
message_button = tk.Button(bottom_frame, text="Send",
                           font=BUTTON_FONT, bg=PASTEL_AQUA, fg=WHITE, command=lambda: send_message(None))
message_textbox.bind('<Return>', send_message)
message_button.pack(side=tk.RIGHT, padx=30)


def main():
    root.mainloop()


if __name__ == '__main__':
    main()
