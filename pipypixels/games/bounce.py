import math
from random import randrange

from pipypixels.games.shared import VectorGameEngine, GameScreen, GameEngine, GameEntity
from pipypixels.graphics.shared import Matrix


class BounceEngine(VectorGameEngine):
    def __init__(self, scale, matrix: Matrix, frame_rate):
        super().__init__(scale, matrix, frame_rate)
        self.__balls = []

    def reset(self):
        self.board.reset()
        self.__draw_walls()
        self.__spawn_balls(100)

    def __spawn_balls(self, count:int):
        for _ in range(count):
            ball = (self.board.get_random_empty_position(),(randrange(0,360),0.5))
            self.__balls.append(ball)

    def __clear_ball(self, position:(float,float)):
        self.board.set(int(position[0]), int(position[1]), GameEntity.EMPTY)

    def __draw_ball(self, position:(float,float)):
        self.board.set(int(position[0]), int(position[1]), GameEntity.BALL)

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
        for i in range(len(self.__balls)):
            ball = self.__balls[i]
            next_pos_and_vector = self.__calculate_next_position_and_vector(ball[0], ball[1])
            # __clear_ball
            self.__clear_ball(ball[0])
            # update ball pos
            self.__balls[i] = next_pos_and_vector
            # __draw_ball
            self.__draw_ball(next_pos_and_vector[0])

    @staticmethod
    def __angle_overflow(angle:float)->float:
        if angle < 0:
            return angle + 360
        if angle >= 360:
            return angle - 360
        return angle

    def __calculate_next_position_and_vector(self, position:(float, float), vector:(float, float))->((float,float),(float,float)):
        a = vector[0]
        v = vector[1]
        x = position[0]
        y = position[1]
        nx = x + (math.cos(math.radians(a - 90)) * v)
        ny = y + (math.sin(math.radians(a - 90)) * v)
        my = self.board.height() / 2
        mx = self.board.width() / 2
        dx = mx - x
        dy = my - y
        if nx <= 1:
            nx = 1
            a = self.__angle_overflow(360 - a) + dy

        if nx >= self.board.width() - 2:
            nx = self.board.width() - 2
            a = self.__angle_overflow(360 - a) + dy

        if ny <= 1:
            ny = 1
            a = self.__angle_overflow(180 - a) + dx

        if ny >= self.board.height() - 2:
            ny = self.board.height() - 2
            a = self.__angle_overflow(180 - a) + dx

        return (nx, ny),(a, v)

class BounceScreen(GameScreen):
    def __init__(self, matrix: Matrix):
        super().__init__(matrix, self.__get_engine, redraw_on_show=True)

    def __get_engine(self) ->GameEngine:
        return BounceEngine(self._scale, self._matrix, 100)