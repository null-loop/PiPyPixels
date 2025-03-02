import sys
import time

from pipypixels.graphics.matrix import ScreenMatrix
from pipypixels.games.life import GameOfLifeEngine
from pipypixels.graphics.shared import ScreenMatrixConfiguration

config = ScreenMatrixConfiguration()
matrix = ScreenMatrix(config)
life = GameOfLifeEngine(2, matrix, 24)

try:
    print("Press CTRL-C to stop.")
    life.random_spawn(5)
    life.begin()
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    life.end()
    sys.exit(0)
