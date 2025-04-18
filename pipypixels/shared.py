import json

from pipypixels.games.bounce import BounceScreen, BounceConfiguration
from pipypixels.games.life import GameOfLifeScreen, GameOfLifeConfiguration
from pipypixels.games.maze import MazeScreen, MazeConfiguration
from pipypixels.games.snakes import SnakeScreen, SnakeConfiguration
from pipypixels.gitstatus import GitStatusConfiguration, GitStatusScreen
from pipypixels.graphics.shared import Matrix
from pipypixels.screens import ScreenController, ArtworkScreen, StartupImageScreen, ArtworkConfiguration
from pipypixels.spotify import SpotifyConfiguration, SpotifyScreen


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
            artwork_config = ArtworkConfiguration.create_from_json(screen_config)
            screen = ArtworkScreen(artwork_config, matrix)
        elif screen_type == "bounce":
            bounce_config = BounceConfiguration.create_from_json(screen_config)
            screen = BounceScreen(bounce_config, matrix)
        elif screen_type == "snake":
            snake_config = SnakeConfiguration.create_from_json(screen_config)
            screen = SnakeScreen(snake_config, matrix)
        elif screen_type == "maze":
            maze_config = MazeConfiguration.create_from_json(screen_config)
            screen = MazeScreen(maze_config, matrix)
        elif screen_type == "game-of-life":
            game_of_life_config = GameOfLifeConfiguration.create_from_json(screen_config)
            screen = GameOfLifeScreen(game_of_life_config, matrix)
        elif screen_type == "spotify":
            spotify_config = SpotifyConfiguration.create_from_json(screen_config)
            screen = SpotifyScreen(spotify_config, matrix)
        elif screen_type == "git-status":
            gitstatus_config = GitStatusConfiguration.create_from_json(screen_config)
            screen = GitStatusScreen(gitstatus_config, matrix)

        if screen is not None:
            screen_controller.add_screen(screen)