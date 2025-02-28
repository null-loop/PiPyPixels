import sys
import time

from PIL import Image

from pipypixels.graphics.matrix import ScreenMatrixConfiguration, ScreenMatrix

config = ScreenMatrixConfiguration()
matrix = ScreenMatrix(config)

try:
    print("Press CTRL-C to stop.")
    matrix.render_image(Image.open("../assets/led.png"))
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    sys.exit(0)