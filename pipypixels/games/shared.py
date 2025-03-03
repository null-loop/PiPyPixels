import math
import queue
import threading
import time
from enum import Enum
from random import randrange

from pipypixels.controls import Command
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
        self.__height = width
        self.__width = height
        self.__scale = scale
        self.__matrix = matrix
        self.__cell_colour_func = cell_colour_func
        for _ in range(width):
            self.__entities.append([GameEntity.EMPTY] * height)

    def get(self, x, y) -> GameEntity:
        if x < 0 or x >= self.__width or y < 0 or y >= self.__height:
            return GameEntity.EMPTY
        return self.__entities[x][y]

    def set(self, x, y, entity_type: GameEntity):
        colour = self.__cell_colour_func(x, y, entity_type)

        self.set_with_colour(x, y, entity_type, colour)

    def set_with_colour(self, x, y, entity_type: GameEntity, colour):
        self.__entities[x][y] = entity_type
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

    def reset(self):
        self.reset_to_type(GameEntity.EMPTY)

    def reset_to_type(self, entity_type: GameEntity):
        for x in range(self.__width):
            for y in range(self.__height):
                self.set(x, y, entity_type)

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
        self.__frame_duration_ns = 1 / frame_rate * 1000000000

    def _calculate_game_board_width(self, led_cols, scale):
        return int(math.floor(led_cols / scale))

    def _calculate_game_board_height(self, led_rows, scale):
        return int(math.floor(led_rows / scale))

    def _colour_cell_func(self, x, y, entity_type:GameEntity):
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
            if not self.__paused:
                self._game_tick()
                frame_duration_ns = time.time_ns() - frame_start
                time_left_ns = self.__frame_duration_ns - frame_duration_ns
                if time_left_ns > 0:
                    time_left_s = time_left_ns / 1000000000
                    time.sleep(time_left_s)
            else:
                time.sleep(1/10)

    def begin(self):
        self.__thread = threading.Thread(target=self.__game_loop)
        self.__thread.start()

    def end(self):
        self.receive_command(Command.EXIT)

    def toggle_pause(self):
        self.receive_command(Command.PAUSE_PLAY)

    def play(self):
        if self.__thread is None:
            self.begin()
        self.receive_command(Command.PLAY)

    def pause(self):
        self.receive_command(Command.PAUSE)

    def _game_tick(self):
        pass

    def receive_command(self, command:Command):
        self.__command_queue.put(command)

class GameScreen(Screen):
    def __init__(self, engine:GameEngine, redraw_on_show=True):
        self._engine = engine
        self.__redraw_on_show = redraw_on_show

    def show(self):
        if self.__redraw_on_show:
            self._engine.board.redraw()
        self._engine.play()

    def hide(self):
        self._engine.pause()

    def receive_command(self, command:Command):
        self._engine.receive_command(command)