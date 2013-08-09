from __future__ import division
from collections import Counter

from kivy.app import App
from kivy.graphics import *
from kivy.properties import (ObjectProperty, ListProperty, NumericProperty,
        BooleanProperty, ReferenceListProperty)
from kivy.uix.scatter import ScatterPlane

import life

BLUE = (0, 0, 1)
CYAN = (0, 1, 1)

class LifeBoard(ScatterPlane):
    cells = ObjectProperty(Counter())
    alive_colour = ListProperty(BLUE)
    aged_cell_colour = ListProperty(CYAN)

    cell_width = NumericProperty(10)
    cell_size = ReferenceListProperty(cell_width, cell_width)
    draw = BooleanProperty(False)

    def update_cells(self):
        self.cells = life.next_iteration(self.cells)

    def on_cells(self, instance, value):
        self.canvas.clear()
        with self.canvas:
            for cell, age in value.items():
                pos = [cell[0]*self.cell_width, cell[1]*self.cell_width]
                Color(*self.interpolate_colour(age))
                Rectangle(size=self.cell_size, pos=pos)

    def interpolate_colour(self, cell_age):
        new_colour = self.old_cell_colour
        old_colour = self.alive_colour
        age = min(cell_age - 1, 16)
        delta = [(new - old)*age/16 for new, old in zip(new_colour, old_colour)]
        colour = [old + d for old, d in zip(old_colour, delta)]
        return colour

    def toggle_draw(self, value):
        self.draw = value == 'down'

    def on_touch_move(self, touch):
        if self.draw:
            cells = self.cells
            cell_width = self.cell_width

            x = touch.x - self.x
            y = touch.y - self.y

            pos = (int(x//cell_width), int(y//cell_width))

            if not cells[pos]:
                cells[pos] = 1
                self.canvas.add(Color(*self.alive_colour))
                cell_pos = (pos[0]*cell_width, pos[1]*cell_width)
                self.canvas.add(Rectangle(size=self.cell_size, pos=cell_pos))

            self.cells = cells
        else:
            super(LifeBoard, self).on_touch_move(touch)

class LifeApp(App):
    pass

if __name__ == '__main__':
    LifeApp().run()
