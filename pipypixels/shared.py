import json

from pipypixels.games.bounce import BounceScreen
from pipypixels.games.life import GameOfLifeScreen
from pipypixels.games.maze import MazeScreen, MazeConfiguration
from pipypixels.games.snakes import SnakeScreen
from pipypixels.graphics.shared import Matrix
from pipypixels.screens import ScreenController, ArtworkScreen, StartupImageScreen


def load_config():
    with open('config/config.json') as json_data:
        return json.load(json_data)

def load_screens(json_config, screen_controller: ScreenController, matrix: Matrix):
    screen_controller.add_screen(StartupImageScreen(matrix))
    screens_config = json_config["screens"]
    for screen_config in screens_config:
        screen_type = screen_config["type"]
        screen = None

        if screen_type == "artwork":
            screen = ArtworkScreen(matrix)
        elif screen_type == "bounce":
            screen = BounceScreen(matrix)
        elif screen_type == "snake":
            screen = SnakeScreen(matrix)
        elif screen_type == "maze":
            maze_config = MazeConfiguration.create_from_json(screen_config)
            screen = MazeScreen(maze_config, matrix)
        elif screen_type == "game-of-life":
            screen = GameOfLifeScreen(matrix)

        if screen is not None:
            screen_controller.add_screen(screen)