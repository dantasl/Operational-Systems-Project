import curses
import time
import sys
from random import randint

class Snake:
    def __init__(self, name):
        self.name = name
        self.direction = curses.KEY_RIGHT        
        self.coords = [[0, 0], [0, 1], [0, 2], [0, 3]]

    def set_field(self, field):
        self.field = field
        
    def set_direction(self, ch):
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

    def is_alive(self):
        head = self.coords[-1]
        snake_body = self.coords[:-1]
        return (head not in snake_body) and (self._is_in_bounds(head))

    def _is_in_bounds(self, point):
        return (point[0] < self.field.size) and (point[0] > -1) and (point[1] > -1) and (point[1] < self.field.size)

    def move(self):
        # Determine head coords
        head = self.coords[-1][:]

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

        # check if snake eat an entity
        if self.field.is_snake_eat_entity(self):
            curses.beep()
            self.level_up()
            self.field.add_entity()