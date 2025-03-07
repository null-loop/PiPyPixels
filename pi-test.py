import sys

from pipypixels.controls.shared import Command
from pipypixels.graphics.pi import ScreenMatrix
from pipypixels.graphics.shared import MatrixConfiguration
from pipypixels.screens import StartupImageScreen

config = MatrixConfiguration()
matrix = ScreenMatrix(config)
screen = StartupImageScreen(matrix)
try:
    print("Press CTRL-C to stop.")
except KeyboardInterrupt:
    screen.receive_command(Command.EXIT)
    sys.exit(0)