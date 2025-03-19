import sys
import time

from PIL import Image
# pylint: disable=import-error
from rgbmatrix import RGBMatrix, RGBMatrixOptions

options = RGBMatrixOptions()
options.chain_length = 5
options.rows = 64
options.cols = 64
options.parallel = 1
options.hardware_mapping = 'adafruit-hat-pwm'
options.gpio_slowdown = 5
options.limit_refresh_rate_hz = 0
options.brightness = 100
options.disable_hardware_pulsing = False
options.drop_privileges = False
matrix = RGBMatrix(options=options)

image = Image.open('./assets/img.png')
rgb = image.convert('RGB')
matrix.SetImage(rgb, unsafe=False)

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    sys.exit(0)