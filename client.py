import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
CAN_SEND_MESSAGE = True

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length+= b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

while CAN_SEND_MESSAGE:
    msg = input('Enter the message: ')
    if msg == 'END':
        CAN_SEND_MESSAGE = False
    else:
        send(msg)
# send(DISCONNECT_MESSAGE)               
