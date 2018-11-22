import curses
import time
import sys
import threading
import socket
import pickle
from random import randint
from Snake import Snake
from Field import Field

serverAddress = (socket.gethostname(), 5010)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bufferSize = 4096

def main(screen):
    player = Snake(sys.argv[1])
    playerBytes = pickle.dumps(player)
    clientSocket.connect(serverAddress)
    clientSocket.sendall(playerBytes)

    while True:
        ch = screen.getch()
        if ch == ord('q'):
            clientSocket.shutdown(socket.SHUT_RDWR)
            break
        elif ch == ord('r'):
            clientSocket.sendall(playerBytes)
        elif ch != -1:
            clientSocket.sendall(pickle.dumps(ch))

def gameThread():
    if (len(sys.argv) != 2):
        print("Usage: python {} [player name]".format(sys.argv[0]))
    else:
        curses.wrapper(main)

if __name__=='__main__':
    gt = threading.Thread(target=gameThread)
    gt.start()
