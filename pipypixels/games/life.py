import math

from PIL import Image
from numpy import asarray

from pipypixels.controls.shared import Command
from pipypixels.games.shared import GameEntity, GameEngine, GameScreen
from pipypixels.graphics import assets
from pipypixels.graphics.shared import Matrix


class GameOfLifeEngine(GameEngine):

    def __init__(self, scale, matrix: Matrix, frame_rate):
        self.__preset_index = 0
        super().__init__(scale, matrix, frame_rate)

    def _colour_cell_func(self, x, y, entity_type:GameEntity):
        colour = (0,0,0)
        if entity_type == GameEntity.CELL:
            r = (x / self.board.width()) * 256
            b = (y / self.board.height()) * 256
            g = 50
            colour = [r, g, b]
        return colour

    def __random_spawn(self, fraction):
        self.board.reset()
        total_cells = self.board.height() * self.board.width()
        population = math.floor(total_cells / fraction)
        for _ in range(population):
            pos = self.board.get_random_empty_position()
            self.board.set(pos[0],pos[1],GameEntity.CELL)

    def __spawn_many(self, spawn_positions):
        self.board.reset()
        for pos in spawn_positions:
            x = pos[0]
            y = pos[1]
            if not (x < 0 or x >= self.board.width() or y < 0 or y >= self.board.height()):
                self.board.set(x, y, GameEntity.CELL)

    def _game_tick(self):
        births=[]
        deaths=[]
        for ex in range(self.board.width()):
            for ey in range(self.board.height()):
                current = self.board.get(ex, ey)
                neighbour_count = self.board.count_neighbours(ex, ey)
                if current == GameEntity.CELL:
                    if neighbour_count < 2 or neighbour_count > 3:
                        deaths.append((ex,ey))
                else:
                    if neighbour_count == 3:
                        births.append((ex, ey))
        for b in births:
            self.board.set(b[0], b[1], GameEntity.CELL)
        for d in deaths:
            self.board.set(d[0], d[1], GameEntity.EMPTY)

    def reset(self):
        if self.__preset_index == 0:
            self.__random_spawn(5)
        elif self.__preset_index == 1:
            self.__load_from_image(assets.life_presets['gosper-glider-gun.png'])

    def __load_from_image(self, image:Image):
        data = asarray(image)
        positions = []
        for y in range(len(data)):
            row = data[y]
            for x in range(len(row)):
                p = row[x]
                if p[0] < 100: positions.append((x, y))
        self.__spawn_many(positions)

    def _handle_command(self, command:Command):
        if command == Command.PRESET_1:
            self.__preset_index = 1
            self.reset()
        elif command == Command.PRESET_10:
            self.__preset_index = 0
            self.reset()

class GameOfLifeScreen(GameScreen):
    def __init__(self, matrix: Matrix):
        super().__init__(matrix, self.__get_engine, redraw_on_show=False)

    def __get_engine(self) ->GameEngine:
        return GameOfLifeEngine(self._scale, self._matrix, self._frame_rate)
