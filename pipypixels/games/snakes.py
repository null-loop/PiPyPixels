from enum import Enum
from math import floor
from random import randrange
from typing import List

from PIL import ImageColor

from pipypixels.games.shared import GameEntity, GameBoard, GameEngine, GameScreen
from pipypixels.graphics.shared import Matrix


class SnakeTurnResult(Enum):
    MOVED = 0
    ATE = 1
    DIED = 2
    SPLIT = 3

class ScoredMove:
    dx = 0
    dy = 0
    score = 0

class SnakeTraits:

    def __init__(self):
        self.food_weight = float(2)
        self.wall_weight = float(-1.1)
        self.snake_weight = float(-1.1)

    def mutate(self):
        trait = randrange(3)
        trait_change = randrange(100) / float(200)
        neg = randrange(2)

        if neg == 1:
            trait_change = 0 - trait_change

        if trait == 0: self.food_weight = self.food_weight + trait_change
        if trait == 1: self.wall_weight = self.wall_weight + trait_change
        if trait == 2: self.snake_weight = self.snake_weight + trait_change

class Snake:

    @classmethod
    def spawn_new_snake(cls, x, y, board):
        colour = [randrange(235) + 20,randrange(235) + 20,randrange(235) + 20]
        traits = SnakeTraits()
        return Snake([[x,y]], traits, colour, board)

    @classmethod
    def split_new_snake(cls, new_parts:List, parent_traits, colour, board):
        traits = SnakeTraits()
        traits.snake_weight = parent_traits.snake_weight
        traits.food_weight = parent_traits.food_weight
        traits.wall_weight = parent_traits.wall_weight

        return Snake(new_parts, traits, colour, board)

    def __init__(self, parts:List, traits, colour, board: GameBoard):

        self.__traits = traits

        head_part = parts[0]
        tail_part = parts[-1]

        if len(parts) == 1:
            self.__last_head_position = head_part.copy()
        else:
            self.__last_head_position = parts[1].copy()

        self.__current_head_position = head_part.copy()
        self.__current_tail_position = tail_part.copy()
        self.__parts = parts.copy()
        self.__board = board
        self.__colour = colour
        self.__length_to_split = 30
        self.redraw_on_board()

    def redraw_on_board(self):
        for part in self.__parts:
            self.__board.set_with_colour(part[0], part[1], GameEntity.SNAKE, self.__colour)

    def turn(self)->SnakeTurnResult:
        previous_dx = self.__current_head_position[0] - self.__last_head_position[0]
        previous_dy = self.__current_head_position[1] - self.__last_head_position[1]

        #Score the moves
        move_one = self.__score_move(-1, 0, previous_dx, previous_dy)
        move_two = self.__score_move(1, 0, previous_dx, previous_dy)
        move_three = self.__score_move(0, 1, previous_dx, previous_dy)
        move_four = self.__score_move(0, -1, previous_dx, previous_dy)

        move = move_one
        if move_two.score > move.score: move = move_two
        if move_three.score > move.score: move = move_three
        if move_four.score > move.score: move = move_four

        new_head_position = [self.__current_head_position[0] + move.dx, self.__current_head_position[1] + move.dy]

        self.__overflow_position(new_head_position)

        target_entity = self.__board.get(new_head_position[0], new_head_position[1])

        if target_entity == GameEntity.WALL or target_entity == GameEntity.SNAKE:
            self.__clear_all_parts_from_board()
            return SnakeTurnResult.DIED
        elif target_entity == GameEntity.FOOD:
            # we're going to grow - so we only move the head, not the tail
            self.__move_head(new_head_position)

            new_length = len(self.__parts)
            if new_length == self.__length_to_split:
                return SnakeTurnResult.SPLIT

            return SnakeTurnResult.ATE
        else:
            # we're not growing, so move the head and the tail
            self.__move_head(new_head_position)
            self.__move_tail()
            return SnakeTurnResult.MOVED

    def split(self):
        # split the parts of our current snake into ours and theirs
        split_length = floor(self.__length_to_split / 2)
        my_parts = self.__parts.copy()[:split_length]
        their_parts = self.__parts.copy()[-split_length:]

        # update our parts
        self.__last_head_position = my_parts[1]
        self.__current_head_position = my_parts[0]
        self.__current_tail_position = my_parts[-1]
        self.__parts = my_parts

        # we're going to create a new snake
        new_snake = Snake.split_new_snake(their_parts, self.__traits, self.__colour.copy(), self.__board)
        new_snake.redraw_on_board()
        return new_snake

    def __move_tail(self):
        self.__board.set(self.__current_tail_position[0], self.__current_tail_position[1], GameEntity.EMPTY)

        if len(self.__parts) == 2:
            # if we're only 1 long - our tail is just our head
            self.__current_tail_position = self.__current_head_position.copy()
            self.__parts.pop(-1)
        else:
            # remove the last part
            self.__parts.pop(-1)
            # our tail pos is now the last item
            self.__current_tail_position = self.__parts[-1].copy()

    def __move_head(self, target_position:(int,int)):
        self.__last_head_position = self.__current_head_position.copy()
        self.__current_head_position = target_position
        self.__board.set_with_colour(target_position[0], target_position[1], GameEntity.SNAKE, self.__colour)
        self.__parts.insert(0, target_position)

    def __clear_all_parts_from_board(self):
        for part in self.__parts:
            self.__board.set(part[0], part[1], GameEntity.EMPTY)

    def __score_move(self, dx, dy, previous_dx, previous_dy)->ScoredMove:

        scored_move = ScoredMove()
        scored_move.dx = dx
        scored_move.dy = dy

        if previous_dx == dx and previous_dy == dy:
            current_score = float(0.25)
        else:
            current_score = float(0)

        max_look_ahead = 5
        current_look_ahead = 1
        projected_head_position_x = self.__current_head_position[0]
        projected_head_position_y = self.__current_head_position[1]
        while current_look_ahead <= max_look_ahead:
            projected_head_position_x = projected_head_position_x + dx
            projected_head_position_y = projected_head_position_y + dy

            projected_head_position_x = self.__overflow_x(projected_head_position_x)
            projected_head_position_y = self.__overflow_y(projected_head_position_y)

            projected_entity = self.__board.get(projected_head_position_x, projected_head_position_y)
            projected_weight = float(0)
            if projected_entity == GameEntity.SNAKE: projected_weight = self.__traits.snake_weight
            if projected_entity == GameEntity.WALL: projected_weight = self.__traits.wall_weight
            if projected_entity == GameEntity.FOOD: projected_weight = self.__traits.food_weight
            projected_weight = projected_weight * (1 / current_look_ahead)
            current_score = current_score + projected_weight
            current_look_ahead = current_look_ahead + 1
        scored_move.score = current_score

        return scored_move

    def __overflow_x(self, x):
        if x == self.__board.width():
            return 0
        elif x == -1:
            return self.__board.width() - 1
        else:
            return x

    def __overflow_y(self, y):
        if y == self.__board.height():
            return 0
        elif y == -1:
            return self.__board.height() - 1
        else:
            return y

    def __overflow_position(self, position:(int,int)):
        position[0] = self.__overflow_x(position[0])
        position[1] = self.__overflow_y(position[1])

class SnakeEngine(GameEngine):
    def __init__(self, scale, matrix: Matrix, frame_rate):
        super().__init__(scale, matrix, frame_rate)
        self.__snakes = []

    def starting_spawn(self):
        self.__spawn_foods(100)
        self.__spawn_snakes(10)

    def __spawn_foods(self, count:int):
        if count != 0:
            for i in range(count):
                pos = self.board.get_random_empty_position()
                self.board.set(pos[0], pos[1], GameEntity.FOOD)

    def __spawn_snakes(self, count:int):
        if count != 0:
            for i in range(count):
                pos = self.board.get_random_empty_position()
                snake = Snake.spawn_new_snake(pos[0], pos[1], self.board)
                self.__snakes.append(snake)

    def _colour_cell_func(self, x, y, entity_type):
        colour = (0,0,0)
        if entity_type == GameEntity.SNAKE: colour = ImageColor.getrgb("Green")
        if entity_type == GameEntity.FOOD: colour = ImageColor.getrgb("Yellow")
        if entity_type == GameEntity.WALL: colour = ImageColor.getrgb("Red")
        return colour

    def _game_tick(self):
        food_to_spawn = 0
        for snake in self.__snakes:
            turn_result = snake.turn()
            if turn_result == SnakeTurnResult.ATE:
                food_to_spawn = food_to_spawn + 1
            if turn_result == SnakeTurnResult.SPLIT:
                food_to_spawn = food_to_spawn + 1
                split_snake = snake.split()
                self.__snakes.append(split_snake)
            if turn_result == SnakeTurnResult.DIED:
                self.__snakes.remove(snake)

        self.__spawn_foods(food_to_spawn)
        if len(self.__snakes) < 100:
            self.__spawn_snakes(100 - len(self.__snakes))

    def reset(self):
        self.board.reset()
        self.__snakes.clear()
        self.starting_spawn()

    def redraw_snakes(self):
        for snake in self.__snakes:
            snake.redraw_on_board()

    def reset_on_play(self):
        return False

class SnakeScreen(GameScreen):
    def __init__(self, matrix: Matrix):
        super().__init__(matrix, self.__get_engine, redraw_on_show=True)

    def __get_engine(self) -> GameEngine:
        return SnakeEngine(self._scale, self._matrix, 256)

    def redraw(self):
        self._engine.board.matrix.start_new_canvas()
        self._engine.board.redraw()
        self._engine.redraw_snakes()
        self._engine.board.matrix.finish_canvas()
