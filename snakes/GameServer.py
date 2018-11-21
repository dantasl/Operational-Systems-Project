import curses
import time
import sys
import threading
import socket
import pickle
from random import randint
from Snake import Snake
from Field import Field

boardSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddress = (socket.gethostname(), 50100)
boardSocket.bind(serverAddress)
bufferSize = 4096

size = 25
field = Field(size)

def main(screen):
    screen.timeout(0)

    while True:
        field.render(screen)
        screen.refresh()
        time.sleep(.4)

def socketThread():
    snakesByAdress = {}
    while True:
        dataBytes, addr = boardSocket.recvfrom(bufferSize)
        if (dataBytes):
            data = pickle.loads(dataBytes)
            try:
                ch = int(data)
                snake = snakesByAdress[addr]
                snake.change_direction(ch)
            except:
                new_player = data
                snakesByAdress[addr] = new_player
                field.add_player(new_player)

def gameThread():
    curses.wrapper(main)

if __name__=='__main__':
    st = threading.Thread(target=socketThread)
    gt = threading.Thread(target=gameThread)
    st.start()
    gt.start()
