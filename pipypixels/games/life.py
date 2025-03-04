import math
import random

from PIL import ImageColor

from pipypixels.games.shared import GameEntity, GameEngine, GameScreen
from pipypixels.graphics.shared import Matrix


class GameOfLifeEngine(GameEngine):

    def _colour_cell_func(self, x, y, entity_type:GameEntity):
        colour = ImageColor.getrgb("Black")
        if entity_type == GameEntity.CELL:
            r = (x / self.board.width()) * 256
            b = (y / self.board.height()) * 256
            g = 50
            colour = [r, g, b]
        return colour

    def __random_spawn(self, fraction):
        self.board.reset(set_matrix=False)
        total_cells = self.board.height() * self.board.width()
        population = math.floor(total_cells / fraction)
        positions = []
        for _ in range(population):
            positions.append(self.board.get_random_empty_position())
        for x in range(self.board.width()):
            for y in range(self.board.height()):
                if (x,y) in positions:
                    self.board.set(x, y, GameEntity.CELL)
                else:
                    self.board.set(x, y, GameEntity.EMPTY)

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
        self.__random_spawn(5)

class GameOfLifeScreen(GameScreen):
    def __init__(self, matrix: Matrix):
        super().__init__(matrix, self.__get_engine, redraw_on_show=False)

    def __get_engine(self) ->GameEngine:
        return GameOfLifeEngine(self._scale, self._matrix, 24)
