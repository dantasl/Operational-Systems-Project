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
boardSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bufferSize = 4096

size = 25
field = Field(size)

snakesByAddress = {}

def main(screen):
    screen.timeout(0)

    while True:
        ch = screen.getch()
        if ch == ord('q'):
            break

        field.render(screen)
        time.sleep(.4)

def socketThread():
    boardSocket.bind(serverAddress)
    boardSocket.listen(5)

    conn, addr = boardSocket.accept()

    processThread = threading.Thread(target=newPlayerThread, args=(conn, addr));
    processThread.start()

def newPlayerThread(conn, addr):
    while True:
        dataBytes = conn.recv(bufferSize)
        if dataBytes:
            data = pickle.loads(dataBytes)
            try:
                ch = int(data)
                snake = snakesByAddress[addr]
                if (snake):
                    snake.change_direction(ch)
            except:
                new_player = data
                snakesByAddress[addr] = new_player
                field.add_player(new_player)
            

def gameThread():
    curses.wrapper(main)

if __name__=='__main__':
    st = threading.Thread(target=socketThread)
    gt = threading.Thread(target=gameThread)
    st.start()
    gt.start()
