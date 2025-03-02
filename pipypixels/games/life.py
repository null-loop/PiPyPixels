import math
import random

from PIL import ImageColor

from pipypixels.games.shared import GameEntity, GameEngine


class GameOfLifeEngine(GameEngine):

    def _colour_cell_func(self, x, y, entity_type:GameEntity):
        colour = ImageColor.getrgb("Black")
        if entity_type == GameEntity.CELL:
            r = (x / self._board.width()) * 256
            b = (y / self._board.height()) * 256
            g = 50
            colour = [r, g, b]
        return colour

    def random_spawn(self, fraction):
        self._board.reset()
        total_cells = self._board.height() * self._board.width()
        population = math.floor(total_cells / fraction)
        for p in range(population):
            populated = False
            while not populated:
                x = random.randint(0, self._board.width() - 1)
                y = random.randint(0, self._board.height() - 1)
                e = self._board.get(x, y)
                if e == GameEntity.EMPTY:
                    self._board.set(x, y, GameEntity.CELL)
                    populated = True

    def _game_tick(self):
        births=[]
        deaths=[]
        for ex in range(self._board.width()):
            for ey in range(self._board.height()):
                current = self._board.get(ex, ey)
                neighbour_count = self._board.count_neighbours(ex, ey)
                if current == GameEntity.CELL:
                    if neighbour_count < 2 or neighbour_count > 3:
                        deaths.append((ex,ey))
                else:
                    if neighbour_count == 3:
                        births.append((ex, ey))
        for b in births:
            self._board.set(b[0],b[1],GameEntity.CELL)
        for d in deaths:
            self._board.set(d[0],d[1],GameEntity.EMPTY)
