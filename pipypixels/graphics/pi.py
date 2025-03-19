from PIL import Image
# pylint: disable=import-error
from rgbmatrix import RGBMatrix, RGBMatrixOptions

from pipypixels.graphics.shared import MatrixConfiguration, Matrix


class LEDMatrix(Matrix):
    def __init__(self, config:MatrixConfiguration):
        super().__init__(config)
        self.__options = RGBMatrixOptions()
        self.__options.chain_length = ((config.overall_led_height * config.overall_led_width) /
                                       (config.panel_led_width * config.panel_led_height))
        self.__options.rows = config.panel_led_height
        self.__options.cols = config.panel_led_width
        self.__options.parallel = 1
        self.__options.pixel_mapper_config = config.pixel_mapper_config
        self.__options.hardware_mapping = config.hardware_mapping
        self.__options.gpio_slowdown = config.gpio_slowdown
        self.__options.limit_refresh_rate_hz = config.limit_refresh_rate_hz
        self.__options.brightness = config.brightness
        self.__options.disable_hardware_pulsing = config.disable_hardware_pulsing
        self.__options.drop_privileges = config.drop_privileges
        self.__matrix = RGBMatrix(options=self.__options)
        self.__next_canvas = self.__matrix.CreateFrameCanvas()
        self.__draw_on_canvas = False

    def start_new_canvas(self):
        self.__draw_on_canvas = True

    def finish_canvas(self):
        self.__next_canvas = self.__matrix.SwapOnVSync(self.__next_canvas)
        self.__next_canvas.Clear()
        self.__draw_on_canvas = False

    def render_image(self, image: Image):
        rgb = image.convert('RGB')

        if self.__draw_on_canvas:
            self.__next_canvas.SetImage(rgb, unsafe=False)
        else:
            self.__next_canvas.SetImage(rgb, unsafe=False)
            self.__next_canvas = self.__matrix.SwapOnVSync(self.__next_canvas)
            self.__next_canvas.Clear()

    def set_pixel(self, x, y, r, g, b):
        if self.__draw_on_canvas:
            self.__next_canvas.SetPixel(x, y, r, g, b)
        else:
            self.__matrix.SetPixel(x, y, r, g, b)

    def clear(self):
        self.__matrix.Clear()

    def increase_brightness(self):
        old = self.__matrix.brightness
        self.__matrix.brightness = min(self.__matrix.brightness + 10, 100)
        return old != self.__matrix.brightness

    def decrease_brightness(self):
        old = self.__matrix.brightness
        self.__matrix.brightness = max(self.__matrix.brightness - 10, 1)
        return old != self.__matrix.brightness
