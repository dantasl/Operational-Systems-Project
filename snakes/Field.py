import curses
from random import randint

directions = {
    0: curses.KEY_UP,
    1: curses.KEY_RIGHT,
    2: curses.KEY_DOWN,
    3: curses.KEY_LEFT
}

icons = {
    -2: ' & ', # Fruit
    -1: ' * ', # Snake body
    0: ' . ', # Available space on field
    1: ' 1 ', # Player head #1
    2: ' 2 ', # Player head #2
    3: ' 3 ', # Player head #3
    4: ' 4 ', # Player head #4
    5: ' 5 ', # Player head #5
}

# Board of the game
class Field:
    def __init__(self, size):
        self.size = size
        self.players = []
        self._generate_field()
        self._clear_field()

    def add_player(self, snake):
        snake.set_coords([[3,3],[3,4],[3,5],[3,6]])
        snake.set_number(len(self.players)+1)
        self.players.append(snake)

    def add_fruit(self):        
        while(True):
            x = randint(0, self.size-1)
            y = randint(0, self.size-1)
            fruit = [x, y]
            
            for snake in self.players:
                if fruit in snake.coords:
                    continue
                    
            self.field[x][y] = -2
            break

    def _generate_field(self):
        self.field = [[0 for j in range(self.size)] for i in range(self.size)]

    def _clear_field(self):        
        self.field = [[j if j== -2 else 0 for j in i] for i in self.field]

    def render(self, screen):
        size = self.size
        self._clear_field()

        # Render snake body on the field
        for snake in self.players:
            snake.move()
            if self.is_snake_alive(snake):
                # check if snake eat an entity
                if self.is_snake_eat_fruit(snake):
                    curses.beep()
                    snake.level_up()
                    self.add_fruit()

                for i, j in snake.coords:
                    self.field[i][j] = -1
                head = snake.get_head()
                self.field[head[0]][head[1]] = snake.number

        # Draw the field
        for i in range(size):
            row = ''
            for j in range(size):
                row += icons[self.field[i][j]]

            screen.addstr(i, 0, row)

        if (self.players):
            screen.addstr(size, 0, "{} are playing".format(', '.join(str(p) for p in self.players)), curses.A_STANDOUT)
        else:
            screen.addstr(size, 0, "nobody is playing :(", curses.A_STANDOUT)

    def get_fruit_position(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j] == -2:
                    return [i, j]

        return [-1, -1]

    def is_snake_eat_fruit(self, snake):
        fruit = self.get_fruit_position()
        head = snake.coords[-1]
        return fruit == head

    def _is_in_bounds(self, point):
        return (point[0] < self.size) and (point[0] > -1) and (point[1] < self.size) and (point[1] > -1)

    def is_snake_alive(self, snake):
        head = snake.coords[-1]
        snake_body = snake.coords[:-1]
        return (head not in snake_body) and (self._is_in_bounds(head))