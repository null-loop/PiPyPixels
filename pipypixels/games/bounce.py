import math
from random import randrange

from pipypixels.games.shared import GameScreen, GameEngine, GameEntity, GameConfiguration, GamePreset
from pipypixels.graphics.shared import Matrix

class BounceConfiguration(GameConfiguration):
    presets = []

    @staticmethod
    def create_from_json(screen_json_config):
        config = BounceConfiguration()
        config.presets = BouncePreset.create_many_from_json_config(screen_json_config)
        config.frame_rate = screen_json_config["frame_rate"]
        config.scale = screen_json_config["scale"]
        return config

class BouncePreset(GamePreset):
    ball_count = 10

    @staticmethod
    def create_many_from_json_config(screen_json_config):
        presets = []
        for preset_index in screen_json_config["presets"]:
            preset_json_config = screen_json_config["presets"][preset_index]
            preset = GamePreset.create_from_json_config(preset_json_config)
            if "ball_count" in preset_json_config:
                preset.ball_count = preset_json_config["ball_count"]
            presets.append(preset)
        return presets

class BounceEngine(GameEngine):
    def __init__(self, matrix: Matrix, config: BounceConfiguration):
        super().__init__(matrix, config)
        self.__config = config
        self.__balls = []
        self.__ball_count = 0
        self.apply_preset(0)

    def reset(self):
        self.board.reset()
        self.__balls.clear()
        self.__draw_walls()
        self.__spawn_balls(self.__ball_count)

    def __spawn_balls(self, count:int):
        for _ in range(count):
            ball = (self.board.get_random_empty_position(),(randrange(0,180) - 90,0.6),(randrange(100,250),0,160))
            self.__balls.append(ball)

    def __clear_ball(self, position:(float,float)):
        self.board.set(int(position[0]), int(position[1]), GameEntity.EMPTY)

    def __draw_ball(self, position:(float,float), colour):
        self.board.set_with_colour(int(position[0]), int(position[1]), GameEntity.BALL, colour)

    def redraw_balls(self):
        for ball in self.__balls:
            self.__draw_ball(ball[0],ball[2])

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
            self.__balls[i] = (next_pos_and_vector[0],next_pos_and_vector[1],ball[2])
            # __draw_ball
            self.__draw_ball(next_pos_and_vector[0], ball[2])

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
            a = self.__angle_overflow(360 - a + dy)

        if nx >= self.board.width() - 2:
            nx = self.board.width() - 2
            a = self.__angle_overflow(360 - a + dy)

        if ny <= 1:
            ny = 1
            a = self.__angle_overflow(180 - a + dx)

        if ny >= self.board.height() - 2:
            ny = self.board.height() - 2
            a = self.__angle_overflow(180 - a + dx)

        # adjust for gravity. a tends toward 180
        da = 0.36 if a < 180 else -0.36
        a = a + da

        return (nx, ny),(a, v)

    def reset_on_play(self):
        return False

    def apply_preset(self, preset_index):
        if preset_index >= len(self.__config.presets):
            preset_index = 0
        preset = self.__config.presets[preset_index]
        self.__ball_count = preset.ball_count

class BounceScreen(GameScreen):
    def __init__(self, config: BounceConfiguration, matrix: Matrix):
        self.__config = config
        super().__init__(matrix, self.__get_engine, config, redraw_on_show=True)

    def __get_engine(self) ->GameEngine:
        return BounceEngine(self._matrix, self.__config)

    def redraw(self):
        self._engine.board.matrix.start_new_canvas()
        self._engine.board.redraw()
        self._engine.redraw_balls()
        self._engine.board.matrix.finish_canvas()