import sys
import time

from pipypixels.controls.shared import Command
from pipypixels.graphics.pi import LEDMatrix
from pipypixels.graphics.shared import MatrixConfiguration
from pipypixels.screens import StartupImageScreen

config = MatrixConfiguration()
matrix = LEDMatrix(config)
screen = StartupImageScreen(matrix)
try:
    print("Press CTRL-C to stop.")
    screen.show()
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    screen.receive_command(Command.EXIT)
    sys.exit(0)