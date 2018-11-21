import curses

class Snake:
    def __init__(self, name):
        self.name = name
        self.direction = curses.KEY_RIGHT
        self.coords = []
        self.number = 0        

    def set_direction(self, direction):
        self.direction = direction

    def set_coords(self, coords):
        self.coords = coords

    def set_number(self, number):
        self.number = number

    def get_head(self):
        return self.coords[-1][:]
        
    def change_direction(self, ch):
        # Check if wrong direction
        if ch == curses.KEY_LEFT and self.direction == curses.KEY_RIGHT:
            return
        if ch == curses.KEY_RIGHT and self.direction == curses.KEY_LEFT:
            return
        if ch == curses.KEY_UP and self.direction == curses.KEY_DOWN:
            return
        if ch == curses.KEY_DOWN and self.direction == curses.KEY_UP:
            return 

        self.direction = ch

    def level_up(self):
        # get last point direction
        a = self.coords[0]
        b = self.coords[1]

        tail = a[:]

        if a[0] < b[0]:
            tail[0]-=1
        elif a[1] < b[1]:
            tail[1]-=1
        elif a[0] > b[0]:
            tail[0]+=1
        elif a[1] > b[1]:
            tail[1]+=1

        self.coords.insert(0, tail)

    def move(self):
        # Determine head coords
        head = self.get_head()

        # Calc new head coords
        if self.direction == curses.KEY_UP:
            head[0]-=1
        elif self.direction == curses.KEY_DOWN:
            head[0]+=1
        elif self.direction == curses.KEY_RIGHT:
            head[1]+=1
        elif self.direction == curses.KEY_LEFT:
            head[1]-=1

        del(self.coords[0])
        self.coords.append(head)

    def __str__(self):
        return self.name