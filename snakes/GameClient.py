import curses
import time
import sys
import threading
import socket
import pickle
from random import randint
from Snake import Snake
from Field import Field

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddress = (socket.gethostname(), 50100)
bufferSize = 4096

def main(screen):
    player = Snake("Lucas")
    playerBytes = pickle.dumps(player)
    clientSocket.sendto(playerBytes, serverAddress)

    while True:
        ch = screen.getch()
        if ch == ord('q'):
            break
        elif ch != -1:
            clientSocket.sendto(pickle.dumps(ch), serverAddress)

def gameThread():
    curses.wrapper(main)

if __name__=='__main__':
    gt = threading.Thread(target=gameThread)
    gt.start()
