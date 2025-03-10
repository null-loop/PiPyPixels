import math
from random import randrange

from pipypixels.games.shared import VectorGameEngine, GameScreen, GameEngine, GameEntity
from pipypixels.graphics.shared import Matrix


class BounceEngine(VectorGameEngine):
    def __init__(self, scale, matrix: Matrix, frame_rate):
        super().__init__(scale, matrix, frame_rate)
        self.__ball_pos = (float(0),float(0))
        self.__ball_vector = (float(0),float(0))

    def reset(self):
        self.board.reset()
        self.__draw_walls()
        #self.__ball_pos = self.board.get_random_empty_position()
        #self.__ball_vector = (randrange(0,360),0.5)
        self.__ball_pos = (32,32)
        self.__ball_vector = (240,0.5)
        self.__draw_ball()

    def __clear_ball(self):
        self.board.set(int(self.__ball_pos[0]), int(self.__ball_pos[1]), GameEntity.EMPTY)

    def __draw_ball(self):
        self.board.set(int(self.__ball_pos[0]), int(self.__ball_pos[1]), GameEntity.BALL)

    def _colour_cell_func(self, x, y, entity_type):
        colour = [0,0,0]
        if entity_type == GameEntity.WALL:
            colour = [255,255,255]
        if entity_type == GameEntity.BALL:
            colour = [255,0,0]
        return colour

    def __draw_walls(self):
        for x in range(self.board.width()):
            self.board.set(x, 0, GameEntity.WALL)
            self.board.set(x, self.board.height() - 1, GameEntity.WALL)
        for y in range(self.board.height()):
            self.board.set(0, y, GameEntity.WALL)
            self.board.set(self.board.width() - 1, y, GameEntity.WALL)

    def _game_tick(self):
        # determine next position
        next_pos_and_vector = self.__calculate_next_position_and_vector()
        # __clear_ball
        self.__clear_ball()
        # update ball pos
        self.__ball_pos = next_pos_and_vector[0]
        self.__ball_vector = next_pos_and_vector[1]
        # __draw_ball
        self.__draw_ball()

    def __calculate_next_position_and_vector(self)->((float,float),(float,float)):
        a = self.__ball_vector[0]
        v = self.__ball_vector[1]
        x = self.__ball_pos[0]
        y = self.__ball_pos[1]
        nx = x + (math.cos(a) * v)
        ny = y + (math.sin(a) * v)
        my = self.board.height() / 2
        mx = self.board.width() / 2
        if nx <= 1:
            nx = 1
            d = abs(my - ny)
            na = a + 180
            if na > 360:
                na = na - 360
            elif na < 0:
                na = na + 360

        if nx >= self.board.width() - 2:
            nx = self.board.width() - 2

        if ny <= 1:
            ny = 1

        if ny >= self.board.height() - 2:
            ny = self.board.height() - 2

        return (nx, ny),(a, v)

class BounceScreen(GameScreen):
    def __init__(self, matrix: Matrix):
        super().__init__(matrix, self.__get_engine, redraw_on_show=True)

    def __get_engine(self) ->GameEngine:
        return BounceEngine(self._scale, self._matrix, 24)