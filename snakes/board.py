import curses
import time
import sys
import threading
import socket
from random import randint
from snake import Snake
from field import Field

boardSocket = socket.socket()
host = socket.gethostname()
port = 12345
boardSocket.bind((host, port))

def main(screen):
    screen.timeout(0)
    size = 25
    field = Field(size)
    snake = Snake("Lucas")
    snake.set_field(field)
    field.add_player(snake)

    while True:
        ch = screen.getch()
        if ch == ord('q'):
            break
        elif ch != -1:
            snake.set_direction(ch)

        field.render(screen)

        if (snake.is_alive()):
            snake.move()
            screen.addstr(size, 0, "{} playing".format(snake.name), curses.A_STANDOUT)

        screen.refresh()
        time.sleep(.4)

def socketThread():
    boardSocket.listen(5)
    c, addr = boardSocket.accept()
    data = boardSocket.recv(1024).decode()
    print(data)
    c.close()

def gameThread():
    curses.wrapper(main)

if __name__=='__main__':
    st = threading.Thread(target=socketThread)
    gt = threading.Thread(target=gameThread)
    st.start()
    gt.start()
