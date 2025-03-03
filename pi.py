import sys
import time

from pipypixels.controls.shared import Command
from pipypixels.controls.sources import RemoteKeyboardCommandSource
from pipypixels.games.life import GameOfLifeScreen
from pipypixels.graphics.matrix import ScreenMatrix
from pipypixels.graphics.shared import MatrixConfiguration
from pipypixels.screens import ScreenController, StartupImageScreen

config = MatrixConfiguration()
matrix = ScreenMatrix(config)
controller = ScreenController()
controller.add_screen(StartupImageScreen(matrix))
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
