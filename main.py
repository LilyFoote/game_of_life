from __future__ import division
from collections import Counter

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.properties import (ObjectProperty, ListProperty, NumericProperty,
        BooleanProperty, ReferenceListProperty, BoundedNumericProperty)
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import ScatterPlane, Scatter
from kivy.uix.slider import Slider

from kivy.garden.tickmarker import TickMarker

import life

COLOURS = {
        'Black': (0, 0, 0),
        'Red': (1, 0, 0),
        'Green': (0, 1, 0),
        'Blue': (0, 0, 1),
        'Yellow': (1, 1, 0),
        'Magenta': (1, 0, 1),
        'Cyan': (0, 1, 1),
        'White': (1, 1, 1),
        }

class TickSlider(Slider, TickMarker):
    pass

class PatternBox(FloatLayout):
    life_board = ObjectProperty()
    pattern = ObjectProperty()

    def load_pattern(self, file_path):
        life_board = self.life_board
        self.pattern = pattern = LifePattern(
                life_board=life_board,
                pos=self.pos,
                do_rotation=False,
                do_scale=False)
        pattern.load_pattern(file_path)
        self.add_widget(pattern)

        pattern.rotation = life_board.rotation
        pattern.scale = life_board.scale

    def rotate(self, angle):
        if self.pattern is not None:
            cells = self.pattern.cells
            cells = life.rotate(cells, angle)
            self.pattern.cells = life.normalise(cells)

class LifePattern(Scatter):
    life_board = ObjectProperty()

    cells = ObjectProperty(set())
    cell_width = NumericProperty(10)
    cell_size = ReferenceListProperty(cell_width, cell_width)

    alive_colour = ListProperty()

    def on_cells(self, instance, value):
        self.canvas.clear()
        with self.canvas:
            for cell in value:
                pos = [cell[0]*self.cell_width, cell[1]*self.cell_width]
                Color(*self.alive_colour)
                Rectangle(size=self.cell_size, pos=pos)

    def load_pattern(self, file_path):
        with open(file_path) as pattern:
            self.cells = life.parse_life_1_06(pattern)

    def on_touch_down(self, touch):
        if not self.parent.collide_point(*touch.pos):
            self.parent.remove_widget(self)
        else:
            return super(LifePattern, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.life_board.parent.collide_point(*touch.pos):
            self.life_board.add_pattern(self.cells, self.to_parent(0, 0))
        self.parent.remove_widget(self)

    def on_size(self, instance, value):
        with self.canvas.before:
            Color(0, 0, 1, 0.2)
            Rectangle(size=value)

class LifeBoard(ScatterPlane):
    cells = ObjectProperty(Counter())
    dead_colour = ListProperty()
    alive_colour = ListProperty()
    aged_cell_colour = ListProperty()
    run_time = NumericProperty()

    cell_width = NumericProperty(10)
    cell_size = ReferenceListProperty(cell_width, cell_width)
    draw = BooleanProperty(False)
    erase = BooleanProperty(False)

    def update_cells(self, *args):
        self.cells = life.next_iteration(self.cells)

    def on_cells(self, instance, value):
        self.canvas.clear()
        with self.canvas:
            for cell, age in value.items():
                pos = [cell[0]*self.cell_width, cell[1]*self.cell_width]
                Color(*self.interpolate_colour(age))
                Rectangle(size=self.cell_size, pos=pos)

    def interpolate_colour(self, cell_age):
        new_colour = self.aged_cell_colour
        old_colour = self.alive_colour
        age = min(cell_age - 1, 16)
        delta = [(new - old)*age/16 for new, old in zip(new_colour, old_colour)]
        colour = [old + d for old, d in zip(old_colour, delta)]
        return colour

    def toggle_draw(self, value):
        self.draw = value == 'down'

    def toggle_erase(self, value):
        self.erase = value == 'down'

    def toggle_run(self, value):
        if value == 'down':
            self.update_cells()
            Clock.schedule_interval(self.update_cells, self.run_time)
        else:
            Clock.unschedule(self.update_cells)

    def on_touch_down(self, touch):
        if self.draw or self.erase:
            self.edit_cells(touch)
        else:
            super(LifeBoard, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.draw or self.erase:
            self.edit_cells(touch)
        else:
            super(LifeBoard, self).on_touch_move(touch)

    def edit_cells(self, touch):
        cells = self.cells
        cell_width = self.cell_width

        x, y = self.to_local(*touch.pos)

        pos = (int(x//cell_width), int(y//cell_width))
        cell_pos = (pos[0]*cell_width, pos[1]*cell_width)

        if self.draw and not cells[pos]:
            cells[pos] = 1
            self.canvas.add(Color(*self.alive_colour))
        elif self.erase and cells[pos]:
            cells[pos] = 0
            self.canvas.add(Color(*self.dead_colour))
        else:
            return

        self.canvas.add(Rectangle(size=self.cell_size, pos=cell_pos))

        self.cells = cells

    def add_pattern(self, pattern, pos):
        pos = self.to_local(*pos)
        cell_width = self.cell_width

        delta_x, delta_y  = pos[0]//cell_width, pos[1]//cell_width

        cells = {(cell[0] + delta_x, cell[1] + delta_y): 1 for cell in pattern}
        self.cells.update(cells)

        self.on_cells(self, self.cells)

class LifeApp(App):
    run_time = BoundedNumericProperty(1, min=0.016, max=1)
    dead_colour = ListProperty()
    alive_colour = ListProperty()
    aged_colour = ListProperty()

    def build_config(self, config):
        config.setdefaults('life', {
            'run_time': 0.3,
            'dead_colour': 'Black',
            'alive_colour': 'Red',
            'aged_colour': 'Yellow',
            })

    def on_config_change(self, config, section, key, value):
        if config is self.config:
            if section == 'life':
                if key == 'run_time':
                    self.run_time = float(value)
                elif key == 'dead_colour':
                    self.dead_colour = COLOURS[value]
                elif key == 'alive_colour':
                    self.alive_colour = COLOURS[value]
                elif key == 'aged_colour':
                    self.aged_colour = COLOURS[value]

    def build_settings(self, settings):
        with open('data/settings/life.json', encoding='utf-8') as f:
            json_data = f.read()
        settings.add_json_panel("Conway's Game of Life",
                            self.config, data=json_data)

    def build(self):
        config = self.config
        self.run_time = config.getfloat('life', 'run_time')
        self.dead_colour = COLOURS[config.get('life', 'dead_colour')]
        self.alive_colour = COLOURS[config.get('life', 'alive_colour')]
        self.aged_colour = COLOURS[config.get('life', 'aged_colour')]

if __name__ == '__main__':
    LifeApp().run()
