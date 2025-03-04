import math
import queue
import threading
import time
from enum import Enum
from random import randrange
from typing import List

from pipypixels.controls.shared import Command
from pipypixels.graphics.shared import Matrix
from pipypixels.screens import Screen


class GameEntity(Enum):
    EMPTY = 0
    WALL = 1
    SNAKE = 2
    FOOD = 3
    CELL = 3
    SOLVER = 5

class GameBoard:
    def __init__(self, width, height, scale, matrix, cell_colour_func):
        self.__entities = []
        self.__height = height
        self.__width = width
        self.__scale = scale
        self.__matrix = matrix
        self.__cell_colour_func = cell_colour_func
        for _ in range(width):
            self.__entities.append([GameEntity.EMPTY] * height)

    def get(self, x, y) -> GameEntity:
        if x < 0 or x >= self.__width or y < 0 or y >= self.__height:
            return GameEntity.EMPTY
        return self.__entities[x][y]

    def set(self, x, y, entity_type: GameEntity, set_matrix=True):
        colour = self.__cell_colour_func(x, y, entity_type)

        self.set_with_colour(x, y, entity_type, colour, set_matrix)

    def set_with_colour(self, x, y, entity_type: GameEntity, colour, set_matrix=True):
        self.__entities[x][y] = entity_type
        if not set_matrix:
            return
        sx = x * self.__scale
        sy = y * self.__scale
        for rx in range(self.__scale):
            for ry in range(self.__scale):
                self.__matrix.set_pixel(rx + sx, ry + sy, colour[0], colour[1], colour[2])

    def get_random_empty_position(self):
        # Randomise x,y until you find an empty location
        while True:
            x = self.__get_random_x()
            y = self.__get_random_y()
            if self.get(x,y) == GameEntity.EMPTY:
                return x,y

    def count_neighbours(self, x, y):
        count = 0
        if x > 0:
            count += self.is_neighbour(x - 1, y - 1)
            count += self.is_neighbour(x - 1, y)
            count += self.is_neighbour(x - 1, y + 1)
        count += self.is_neighbour(x, y - 1)
        count += self.is_neighbour(x, y + 1)
        if x < self.__width - 1:
            count += self.is_neighbour(x + 1, y - 1)
            count += self.is_neighbour(x + 1, y)
            count += self.is_neighbour(x + 1, y + 1)
        return count

    def is_neighbour(self, x, y)->int:
        if y < 0 or y >= self.__height:
            return 0
        if self.__entities[x][y] == GameEntity.CELL:
            return 1
        return 0

    def __add_if_entity_type(self,x,y,entity_type:GameEntity,target:List):
        if self.get(x,y) == entity_type:target.append((x,y))

    def get_immediate_neighbours(self, x, y, entity_type:GameEntity)->List:
        neighbours = []
        if x > 0:
            self.__add_if_entity_type(x - 1, y,entity_type,neighbours)
        self.__add_if_entity_type(x, y - 1,entity_type,neighbours)
        self.__add_if_entity_type(x, y + 1,entity_type,neighbours)
        if x < self.__width - 1:
            self.__add_if_entity_type(x + 1, y,entity_type,neighbours)
        return neighbours

    def reset(self, set_matrix=True):
        self.reset_to_type(GameEntity.EMPTY, set_matrix)

    def reset_to_type(self, entity_type: GameEntity, set_matrix=True):
        for x in range(self.__width):
            for y in range(self.__height):
                self.set(x, y, entity_type, set_matrix)

    def redraw(self):
        for x in range(self.__width):
            for y in range(self.__height):
                e = self.get(x, y)
                self.set(x, y, e)

    def width(self)->int:
        return self.__width

    def height(self)->int:
        return self.__height

    def __get_random_x(self)->int:
        return randrange(self.width())

    def __get_random_y(self)->int:
        return randrange(self.height())

class GameEngine:
    def __init__(self, scale, matrix: Matrix, frame_rate):
        width = self._calculate_game_board_width(matrix.config.overall_led_cols, scale)
        height = self._calculate_game_board_height(matrix.config.overall_led_rows, scale)
        self.board = GameBoard(width, height, scale, matrix, self._colour_cell_func)
        self.__thread = None
        self.__command_queue = queue.Queue()
        self.__paused = False
        self.__step_forward = False
        self.__frame_rate = frame_rate
        self.__update_frame_duration_from_rate()

    def _calculate_game_board_width(self, led_cols, scale):
        return int(math.floor(led_cols / scale))

    def _calculate_game_board_height(self, led_rows, scale):
        return int(math.floor(led_rows / scale))

    def _colour_cell_func(self, x, y, entity_type:GameEntity):
        pass

    def __update_frame_duration_from_rate(self):
        self.__frame_duration_ns = 1 / self.__frame_rate * 1000000000

    def reset(self):
        pass

    def __game_loop(self):
        while True:
            frame_start = time.time_ns()
            if not self.__command_queue.empty():
                command = self.__command_queue.get()
                if command == Command.EXIT:
                    return
                if command == Command.PAUSE_PLAY:
                    self.__paused = not self.__paused
                if command == Command.PLAY:
                    self.__paused = False
                if command == Command.PAUSE:
                    self.__paused = True
                if command == Command.STEP_FORWARD:
                    self.__step_forward = True
                if command == Command.FRAMERATE_UP:
                    self.__frame_rate = self.__frame_rate + 1
                    self.__update_frame_duration_from_rate()
                if command == Command.FRAMERATE_DOWN:
                    self.__frame_rate = max(self.__frame_rate - 1, 1)
                    self.__update_frame_duration_from_rate()
                if command == Command.RESET:
                    self.reset()
            if not self.__paused or self.__step_forward:
                self.__step_forward = False
                self._game_tick()
                frame_duration_ns = time.time_ns() - frame_start
                time_left_ns = self.__frame_duration_ns - frame_duration_ns
                if time_left_ns > 0:
                    time_left_s = time_left_ns / 1000000000
                    time.sleep(time_left_s)
            else:
                time.sleep(1/10)

    def is_paused(self):
        return self.__paused

    def begin(self):
        self.__thread = threading.Thread(target=self.__game_loop)
        self.__thread.start()

    def end(self):
        self.receive_command(Command.EXIT)

    def toggle_pause(self):
        self.receive_command(Command.PAUSE_PLAY)

    def play(self):
        if self.__thread is None:
            self.receive_command(Command.RESET)
            self.begin()
        elif self.reset_on_play():
            self.receive_command(Command.RESET)
        self.receive_command(Command.PLAY)

    def pause(self):
        self.receive_command(Command.PAUSE)

    def _game_tick(self):
        pass

    def receive_command(self, command:Command):
        self.__command_queue.put(command)

    def reset_on_play(self):
        return True

class GameScreen(Screen):
    _scale = 1
    def __init__(self, matrix: Matrix, engine_func, redraw_on_show=True):
        self.__redraw_on_show = redraw_on_show
        self._matrix = matrix
        self._engine = engine_func()
        self.__engine_func = engine_func
        self._scale = 1

    def show(self):
        self._matrix.clear()
        if self.__redraw_on_show:
            self._engine.board.redraw()
        self._engine.play()

    def hide(self):
        self._engine.pause()

    def __rebuild_engine(self):
        self._engine.pause()
        while not self._engine.is_paused():
            time.sleep(1/1000)
        self._engine.end()
        self._matrix.clear()
        self._engine = self.__engine_func()
        self._engine.play()

    def receive_command(self, command:Command):
        if command == Command.ZOOM_IN:
            self._scale = min(self._scale + 1, 8)
            self.__rebuild_engine()
        elif command == Command.ZOOM_OUT:
            self._scale = max(self._scale - 1, 1)
            self.__rebuild_engine()
        else:
            self._engine.receive_command(command)

    def is_paused(self):
        return self._engine.is_paused()

    def redraw(self):
        self._engine.board.redraw()