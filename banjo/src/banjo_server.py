import socket
import subprocess
from threading import *

HOST = "192.168.0.23"
PORT = 65432

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(5)


class Client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        while 1:
            data = self.sock.recv(1024).decode()
            if not data:
                break
            print("Instruction: {}".format(data))
            if data == "UP":
                subprocess.run(["xdotool", "key", "Up"])
            elif data == "DOWN":
                subprocess.run(["xdotool", "key", "Down"])
            elif data == "LEFT":
                subprocess.run(["xdotool", "key", "Left"])
            elif data == "RIGHT":
                subprocess.run(["xdotool", "key", "Right"])
            self.sock.sendall(b'Instruction received.')


while True:
    clientSocket, address = serverSocket.accept()
    Client(clientSocket, address)
