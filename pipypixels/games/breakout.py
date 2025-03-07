from pipypixels.games.shared import VectorGameEngine, GameScreen, GameEngine, GameEntity
from pipypixels.graphics.shared import Matrix


class BreakoutEngine(VectorGameEngine):
    def __init__(self, scale, matrix: Matrix, frame_rate):
        super().__init__(scale, matrix, frame_rate)

    def reset(self):
        self.board.reset()

    def _colour_cell_func(self, x, y, entity_type):
        colour = [0,0,0]
        if entity_type == GameEntity.WALL:
            colour = [255,255,255]
        return colour

    def __draw_walls(self):
        for x in range(self.board.width()):
            self.board.set(x, 0, GameEntity.WALL)
            self.board.set(x, self.board.height() - 1, GameEntity.WALL)
        for y in range(self.board.height()):
            self.board.set(0, y, GameEntity.WALL)
            self.board.set(self.board.width() - 1, y, GameEntity.WALL)

class BreakoutScreen(GameScreen):
    def __init__(self, matrix: Matrix):
        super().__init__(matrix, self.__get_engine, redraw_on_show=True)

    def __get_engine(self) ->GameEngine:
        return BreakoutEngine(self._scale, self._matrix, 24)