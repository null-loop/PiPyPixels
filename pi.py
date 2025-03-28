import sys
import time

from pipypixels.controls.shared import Command
from pipypixels.controls.pi import RemoteKeyboardCommandSource
from pipypixels.games.bounce import BounceScreen
from pipypixels.games.life import GameOfLifeScreen
from pipypixels.games.maze import MazeScreen
from pipypixels.games.snakes import SnakeScreen
from pipypixels.graphics.pi import LEDMatrix
from pipypixels.graphics.shared import MatrixConfiguration
from pipypixels.screens import ScreenController, StartupImageScreen, ArtImageScreen

config = MatrixConfiguration.load('config/config.json')
matrix = LEDMatrix(config)
controller = ScreenController(matrix)
controller.add_screen(StartupImageScreen(matrix))
controller.add_screen(ArtImageScreen(matrix))
controller.add_screen(BounceScreen(matrix))
controller.add_screen(SnakeScreen(matrix))
controller.add_screen(MazeScreen(matrix))
controller.add_screen(GameOfLifeScreen(matrix))
command_source = RemoteKeyboardCommandSource(controller)

try:
    print("Press CTRL-C to stop.")
    controller.begin()
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    controller.receive_command(Command.EXIT)
    sys.exit(0)
