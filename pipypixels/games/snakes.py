from enum import Enum
from math import floor
from random import randrange
from typing import List

from PIL import ImageColor

from pipypixels.controls.shared import Command
from pipypixels.games.shared import GameEntity, GameBoard, GameEngine, GameScreen, GameConfiguration, GamePreset
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
        self.length_to_split = 30
        self.max_look_ahead = 5
        self.turns_to_starvation = 0

    def mutate(self):
        trait = randrange(3)
        trait_change = randrange(100) / float(200)
        neg = randrange(2)

        if neg == 1:
            trait_change = 0 - trait_change

        if trait == 0: self.food_weight = self.food_weight + trait_change
        if trait == 1: self.wall_weight = self.wall_weight + trait_change
        if trait == 2: self.snake_weight = self.snake_weight + trait_change

class SnakeConfiguration(GameConfiguration):
    presets = []

    @staticmethod
    def create_from_json(screen_json_config):
        config = SnakeConfiguration()
        config.presets = SnakePreset.create_many_from_json_config(screen_json_config)
        config.frame_rate = screen_json_config["frame_rate"]
        config.scale = screen_json_config["scale"]
        return config

class SnakePreset(GamePreset):
    snake_count = 20
    food_count = 100
    traits = SnakeTraits()

    @staticmethod
    def create_many_from_json_config(screen_json_config):
        presets = []
        for preset_index in screen_json_config["presets"]:
            preset_json_config = screen_json_config["presets"][preset_index]
            preset = GamePreset.create_from_json_config(preset_json_config)
            if "snake_count" in preset_json_config:
                preset.snake_count = preset_json_config["snake_count"]
            if "food_count" in preset_json_config:
                preset.food_count = preset_json_config["food_count"]
            presets.append(preset)
        return presets

class Snake:

    @classmethod
    def spawn_new_snake(cls, x, y, board, traits: SnakeTraits):
        colour = [randrange(235) + 20,randrange(235) + 20,randrange(235) + 20]

        return Snake([[x,y]], traits, colour, board)

    @classmethod
    def split_new_snake(cls, new_parts:List, parent_traits, colour, board):
        traits = SnakeTraits()
        traits.snake_weight = parent_traits.snake_weight
        traits.food_weight = parent_traits.food_weight
        traits.wall_weight = parent_traits.wall_weight
        traits.length_to_split = parent_traits.length_to_split
        traits.turns_to_starvation = parent_traits.turns_to_starvation

        return Snake(new_parts, traits, colour, board)

    def __init__(self, parts:List, traits, colour, board: GameBoard):

        self.__traits = traits
        self.__turns_since_last_ate = 0

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
        self.__length_to_split = traits.length_to_split
        self.redraw_on_board()

    def redraw_on_board(self):
        for part in self.__parts:
            self.__board.set_with_colour(part[0], part[1], GameEntity.SNAKE, self.__colour)

    def __can_move(self,dx,dy)->bool:
        position = [self.__current_head_position[0] + dx,self.__current_head_position[1] + dy]
        self.__overflow_position(position)
        entity = self.__board.get(position[0], position[1])
        return entity == GameEntity.EMPTY or entity == GameEntity.FOOD

    def turn(self)->SnakeTurnResult:
        previous_dx = self.__current_head_position[0] - self.__last_head_position[0]
        previous_dy = self.__current_head_position[1] - self.__last_head_position[1]

        possible_moves = []
        # Score any possible moves
        if self.__can_move(-1,0):
            possible_moves.append(self.__score_move(-1, 0, previous_dx, previous_dy))
        if self.__can_move(1,0):
            possible_moves.append(self.__score_move(1, 0, previous_dx, previous_dy))
        if self.__can_move(0,1):
            possible_moves.append(self.__score_move(0, 1, previous_dx, previous_dy))
        if self.__can_move(0,-1):
            possible_moves.append(self.__score_move(0, -1, previous_dx, previous_dy))

        if len(possible_moves) == 0:
            # death!
            self.__clear_all_parts_from_board()
            return SnakeTurnResult.DIED
        else:
            # pick the best move and apply it
            move = None
            for possible_move in possible_moves:
                if move is None or move.score < possible_move.score:
                    move = possible_move

            new_head_position = [self.__current_head_position[0] + move.dx, self.__current_head_position[1] + move.dy]

            self.__overflow_position(new_head_position)

            target_entity = self.__board.get(new_head_position[0], new_head_position[1])

            if target_entity == GameEntity.FOOD:
                # we're going to grow - so we only move the head, not the tail
                self.__turns_since_last_ate = 0
                self.__move_head(new_head_position)

                new_length = len(self.__parts)
                if new_length == self.__length_to_split:
                    return SnakeTurnResult.SPLIT

                return SnakeTurnResult.ATE
            else:
                self.__turns_since_last_ate = self.__turns_since_last_ate + 1
                # check if we're starving...
                if 0 < self.__traits.turns_to_starvation < self.__turns_since_last_ate:
                    if len(self.__parts) == 1:
                        # starved to death!
                        self.__clear_all_parts_from_board()
                        return SnakeTurnResult.DIED
                    # we need to remove our tail...
                    self.__move_tail()
                    self.__turns_since_last_ate = 0
                    return SnakeTurnResult.MOVED
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

        max_look_ahead = self.__traits.max_look_ahead
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
    def __init__(self, matrix: Matrix, config: SnakeConfiguration):
        super().__init__(matrix, config)
        self.__snakes = []
        self.__food_count = 100
        self.__snake_count = 20
        self.__starting_traits = SnakeTraits()

    def starting_spawn(self):
        self.__spawn_foods(self.__food_count)
        self.__spawn_snakes(self.__snake_count)

    def __spawn_foods(self, count:int):
        if count != 0:
            for i in range(count):
                pos = self.board.get_random_empty_position()
                self.board.set(pos[0], pos[1], GameEntity.FOOD)

    def __spawn_snakes(self, count:int):
        if count != 0:
            for i in range(count):
                pos = self.board.get_random_empty_position()
                snake = Snake.spawn_new_snake(pos[0], pos[1], self.board, self.__starting_traits)
                self.__snakes.append(snake)

    def _colour_cell_func(self, x, y, entity_type):
        colour = (0,0,0)
        if entity_type == GameEntity.SNAKE: colour = (0,255,0)
        if entity_type == GameEntity.FOOD: colour = (255,255,255)
        if entity_type == GameEntity.WALL: colour = (255,0,0)
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
        if len(self.__snakes) < self.__snake_count:
            self.__spawn_snakes(self.__snake_count - len(self.__snakes))

    def reset(self):
        self.board.reset()
        self.__snakes.clear()
        self.starting_spawn()

    def redraw_snakes(self):
        for snake in self.__snakes:
            snake.redraw_on_board()

    def reset_on_play(self):
        return False

    def apply_preset(self, preset_index):
        if preset_index == 0:
            self.__food_count = 100
            self.__snake_count = 20
            self.__starting_traits = SnakeTraits()
        elif preset_index == 1:
            # Very long, risk-averse
            self.__snake_count = 2
            self.__food_count = 200
            self.__starting_traits = SnakeTraits()
            self.__starting_traits.length_to_split = 1000
            self.__starting_traits.snake_weight = -100
            self.__starting_traits.max_look_ahead = 50
        elif preset_index == 2:
            self.__snake_count = 10
            self.__food_count = 50
            self.__starting_traits = SnakeTraits()
            self.__starting_traits.length_to_split = 100
        elif preset_index == 3:
            self.__snake_count = 100
            self.__food_count = 20
            self.__starting_traits = SnakeTraits()
            self.__starting_traits.length_to_split = 10
            self.__starting_traits.turns_to_starvation = 100

class SnakeScreen(GameScreen):
    def __init__(self, config: SnakeConfiguration, matrix: Matrix):
        self.__config = config
        super().__init__(matrix, self.__get_engine, config,redraw_on_show=True)

    def __get_engine(self) -> GameEngine:
        return SnakeEngine(self._matrix, self.__config)

    def redraw(self):
        self._engine.board.matrix.start_new_canvas()
        self._engine.board.redraw()
        self._engine.redraw_snakes()
        self._engine.board.matrix.finish_canvas()
