import math
import sys
import time
from enum import Enum
from random import choice, randrange

from pipypixels.games.shared import GameEntity, GameBoard, GameEngine, GameScreen
from pipypixels.graphics.shared import Matrix


class Junction:
    x = 0
    y = 0
    turns = []

class GameState(Enum):
    NOT_STARTED = 0
    PROGRESSING = 1
    RETURNING = 2

class MazeGenerator:
    _UP = (0,1)
    _LEFT = (-1, 0)
    _RIGHT = (1, 0)
    _DOWN = (0, -1)
    def __init__(self, board: GameBoard):
        self.__board = board
        self.__visited = []
        sys.setrecursionlimit(10000)

    def generate(self):
        self.__visited = [(1, 1)]
        self.__visit(1,1)

    def __visit(self, x, y):
        self.__board.set(x, y, GameEntity.EMPTY)
        while True:
            unvisited = []
            # find which of our neighbouring spaces we've not visited before...
            if y > 1 and self.__board.get(x, y - 2) == GameEntity.WALL:
                unvisited.append(self._UP)
            if y < self.__board.height() - 2 and self.__board.get(x, y + 2) == GameEntity.WALL:
                unvisited.append(self._DOWN)
            if x > 1 and self.__board.get(x - 2, y) == GameEntity.WALL:
                unvisited.append(self._LEFT)
            if x < self.__board.width() - 2 and self.__board.get(x + 2, y) == GameEntity.WALL:
                unvisited.append(self._RIGHT)

            if len(unvisited) == 0:
                # we've hit a dead end
                return
            else:
                next_direction = choice(unvisited)
                next_x = x
                next_y = y

                if next_direction == self._UP:
                    next_y = y - 2
                    self.__board.set(x, y - 1, GameEntity.EMPTY) # connection
                if next_direction == self._DOWN:
                    next_y = y + 2
                    self.__board.set(x, y + 1, GameEntity.EMPTY) # connection
                if next_direction == self._LEFT:
                    next_x = x - 2
                    self.__board.set(x - 1, y, GameEntity.EMPTY) # connection
                if next_direction == self._RIGHT:
                    next_x = x + 2
                    self.__board.set(x + 1, y, GameEntity.EMPTY) # connection

                self.__visit(next_x, next_y)

class MazeEngine(GameEngine):
    def __init__(self, scale, matrix: Matrix, frame_rate):
        super().__init__(scale, matrix, frame_rate)
        self.__maze_entrance = ()
        self.__maze_exit = ()
        self.__trail = []
        self.__junctions = []
        self.__state = GameState.NOT_STARTED
        self.__wait_until = -1
        self.__returning_to = None

    def _calculate_game_board_width(self, led_cols, scale):
        w = int(math.floor(led_cols / scale))
        if w % 2 == 0 : w = w - 1
        return w

    def _calculate_game_board_height(self, led_rows, scale):
        h = int(math.floor(led_rows / scale))
        if h % 2 == 0 : h = h - 1
        return h

    def _colour_cell_func(self, x, y, entity_type):
        colour = [0,0,0]
        if entity_type == GameEntity.WALL:
            colour = [80,80,80]
        if entity_type == GameEntity.SOLVER:
            colour = [0, 255, 0]
        return colour

    def reset(self):
        self.__wait_until = -1
        self.__generate_maze()

    def _game_tick(self):
        if self.__wait_until > 0:
            if time.time() > self.__wait_until:
                self.reset()
        else:
            fin = False
            if self.__state == GameState.NOT_STARTED:
                self.__trail.append(self.__maze_entrance)
                self.board.set(self.__maze_entrance[0], self.__maze_entrance[1], GameEntity.SOLVER)
                self.__state = GameState.PROGRESSING
            elif self.__state == GameState.PROGRESSING:
                current = self.__trail[-1]
                can_move = self.board.get_immediate_neighbours(current[0], current[1], GameEntity.EMPTY)
                # if we've returned to a previous junction - remove the turns we've already taken from the possible moves
                if self.__returning_to is not None:
                    for already_turned in self.__returning_to.turns:
                        can_move.remove(already_turned)
                # 'tis a dead end my lord!
                if len(can_move) == 0:
                    # if we're already returning to a junction, then pop that junction as it's exhausted
                    if self.__returning_to is not None:
                        self.__junctions.pop()
                    # we're now returning to the next junction in our back track
                    self.__state = GameState.RETURNING
                    if len(self.__junctions) == 0:
                        fin = True # this should never happen!
                    else:
                        self.__returning_to = self.__junctions[-1]
                else:
                    if self.__maze_exit in can_move:
                        fin = True
                    else:
                        next_move = can_move[0]
                        if self.__returning_to is not None:
                            # now record the next turn we're making
                            self.__returning_to.turns.append(next_move)
                            self.__returning_to = None
                        else:
                            # if this is a junction we need to add that to our list
                            if len(can_move) > 1:
                                junction = Junction()
                                junction.x = current[0]
                                junction.y = current[1]
                                junction.turns = [next_move]
                                self.__junctions.append(junction)
                        self.__trail.append(next_move)
                        self.board.set(next_move[0], next_move[1], GameEntity.SOLVER)
            elif self.__state == GameState.RETURNING:
                current = self.__trail[-1]
                if current[0] == self.__returning_to.x and current[1] == self.__returning_to.y:
                    self.__state = GameState.PROGRESSING
                else:
                    trimmed = self.__trail.pop()
                    self.board.set_with_colour(trimmed[0], trimmed[1], GameEntity.EMPTY, [0, 60, 0])

            # check when we've solved the maze - and start another one!
            if fin:
                self.board.set(self.__maze_exit[0], self.__maze_exit[1], GameEntity.SOLVER)
                self.__wait_until = time.time() + 10 # display the solution for 10s before resetting

    def __generate_maze(self):
        # reset the board to all walls
        self.board.reset_to_type(GameEntity.WALL)
        # reset game state
        self.__trail.clear()
        self.__junctions.clear()
        self.__state = GameState.NOT_STARTED
        self.__returning_to = None
        # The generator runs in here - write to the board as it goes
        generator = MazeGenerator(self.board)
        generator.generate()
        # Then pick an entrance and an exit - carve from board - set __maze_entrance and __maze_exit
        found_entrance = False
        while not found_entrance:
            pos_y = randrange(self.board.height())
            if self.board.get(1, pos_y) == GameEntity.EMPTY:
                found_entrance = True
                self.__maze_entrance = (0, pos_y)
                self.board.set(0, pos_y, GameEntity.EMPTY)

        found_exit = False
        while not found_exit:
            pos_y = randrange(self.board.height())
            if self.board.get(self.board.width() - 2, pos_y) == GameEntity.EMPTY:
                found_exit = True
                self.__maze_exit = (self.board.width() - 1, pos_y)
                self.board.set(self.board.width() - 1, pos_y, GameEntity.EMPTY)

class MazeScreen(GameScreen):
    def __init__(self, matrix: Matrix):
        super().__init__(matrix, self.__get_engine, redraw_on_show=False)

    def __get_engine(self) ->GameEngine:
        return MazeEngine(self._scale, self._matrix, 256)