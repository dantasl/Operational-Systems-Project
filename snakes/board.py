import curses
import time
import sys
import threading
import socket
from random import randint
from snake import Snake

boardSocket = socket.socket()
host = socket.gethostname()
port = 12345
boardSocket.bind((host, port))

class Field:
    def __init__(self, size):
        self.size = size
        self.icons = {
            0: ' . ',
            1: ' * ',
            2: ' # ',
            3: ' & ',
        }
        self.players = []
        self._generate_field()
        self.add_entity()

    def add_player(self, snake):
        self.players.append(snake)

    def add_entity(self):        
        while(True):
            i = randint(1, self.size-1)
            j = randint(1, self.size-1)
            entity = [i, j]
            
            occupied = False;
            for snake in self.players:
                if entity in snake.coords:
                    occupied = True;
                    
            if not occupied:
                self.field[i][j] = 3
                break

    def _generate_field(self):
        self.field = [[0 for j in range(self.size)] for i in range(self.size)]

    def _clear_field(self):        
        self.field = [[j if j!= 1 and j!= 2 else 0 for j in i] for i in self.field]

    def render(self, screen):
        size = self.size
        self._clear_field()

        # Render snake on the field
        for snake in self.players:
            for i, j in snake.coords:
                self.field[i][j] = 1

        # Mark head
        for snake in self.players:
            if (snake.coords):
                head = snake.coords[-1]
                self.field[head[0]][head[1]] = 2

        for i in range(size):
            row = ''
            for j in range(size):
                row += self.icons[self.field[i][j]]

            screen.addstr(i, 0, row)

    def get_entity_pos(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j] == 3:
                    return [i, j]

        return [-1, -1]

    def is_snake_eat_entity(self, snake):
        entity = self.get_entity_pos()
        head = snake.coords[-1]
        return entity == head

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
