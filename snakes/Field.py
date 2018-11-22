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
        self.dead_players = []
        self.field = []
        self._generate_field()
        self._clear_field()

    def add_player(self, snake):
        direction = directions[randint(0, 3)]
        snake.set_direction(direction)

        while True:
            coords = self._generate_random_coords(direction)
            if (self._points_are_available(coords)):
                snake.set_coords(coords)
                break

        snake.set_number(len(self.players)+1)
        self.players.append(snake)

    def add_fruit(self):        
        while True:
            x = randint(0, self.size-1)
            y = randint(0, self.size-1)
            fruit = [x, y]
            print("{} {}".format(x, y))
            
            for snake in self.players:
                if fruit in snake.coords:
                    continue
                    
            self.field[x][y] = -2
            break

    def _generate_random_coords(self, direction):
        x = randint(5, self.size-5)
        y = randint(5, self.size-5)

        if direction == curses.KEY_LEFT:
            return [[x-i,y] for i in range(4)]
        elif direction == curses.KEY_RIGHT:
            return [[x+i,y] for i in range(4)]
        elif direction == curses.KEY_UP:
            return [[x,y-i] for i in range(4)]
        elif direction == curses.KEY_DOWN:
            return [[x,y+i] for i in range(4)]

    def _points_are_available(self, collection):
        for x, y in collection:
            if self.field[x][y] != 0:
                return False
        return True

    def _generate_field(self):
        self.field = [[0 for j in range(self.size)] for i in range(self.size)]

    def _clear_field(self):        
        self.field = [[j if j == -2 else 0 for j in i] for i in self.field]

    def render(self, screen):
        size = self.size
        self._clear_field()

        # Render snakes on the field
        for snake in self.players:
            snake.move()
            if self.is_snake_alive(snake):
                if self.is_snake_eat_fruit(snake):
                    curses.beep()
                    snake.level_up()
                    self.add_fruit()

                for i, j in snake.coords:
                    self.field[i][j] = -1
                head = snake.get_head()
                self.field[head[0]][head[1]] = snake.number
            else:
                self.players.remove(snake)
                self.dead_players.append(snake)

        # Draw the field
        for i in range(size):
            row = ''
            for j in range(size):
                row += icons[self.field[i][j]]

            screen.addstr(i, 0, row)

        if (self.players):
            screen.clrtoeol()
            screen.refresh()
            screen.addstr(size, 0, "playing: {}".format(', '.join(str(p) for p in self.players)), curses.A_STANDOUT)

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