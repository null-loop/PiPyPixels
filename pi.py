import sys
import time

from pipypixels.controls.pi import RemoteKeyboardCommandSource
from pipypixels.controls.shared import Command
from pipypixels.graphics.pi import LEDMatrix
from pipypixels.graphics.shared import MatrixConfiguration
from pipypixels.screens import ScreenController
from pipypixels.shared import load_config, load_screens

all_config = load_config()
matrix_config = MatrixConfiguration.create_from_json(all_config)
matrix = LEDMatrix(matrix_config)
controller = ScreenController(matrix)

load_screens(all_config, controller, matrix)

command_source = RemoteKeyboardCommandSource(controller)

try:
    print("Press CTRL-C to stop.")
    controller.begin()
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    controller.receive_command(Command.EXIT)
    sys.exit(0)
