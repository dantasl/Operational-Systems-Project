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
bufferSize = 8192

size = 25
field = Field(size)

snakesByAddress = {}

def main(screen):
    screen.timeout(0)
    field.add_fruit()

    while True:
        ch = screen.getch()
        if ch == ord('q'):
            break

        field.render(screen)
        time.sleep(.4)

    boardSocket.shutdown(2)
    boardSocket.close()

def socketThread():
    boardSocket.bind(serverAddress)
    boardSocket.listen(5)

    while len(snakesByAddress) < 5:
        try:
            conn, addr = boardSocket.accept()

            thread1 = threading.Thread(target=newPlayerThread, args=(conn, addr));
            thread1.start()

            thread2 = threading.Thread(target=shareBoardThread, args=(conn, addr));
            thread2.start()
        except:
            pass

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
    conn.shutdown(2)
    conn.close()

def shareBoardThread(conn, addr):
    while True:
        fieldBytes = pickle.dumps(field)
        try:
            conn.send(fieldBytes)
        except:
            pass
        time.sleep(.4)

def gameThread():
    curses.wrapper(main)

if __name__=='__main__':
    st = threading.Thread(target=socketThread)
    gt = threading.Thread(target=gameThread)
    st.start()
    gt.start()
