from PIL import Image
# pylint: disable=import-error
from rgbmatrix import RGBMatrix, RGBMatrixOptions

from pipypixels.graphics.shared import MatrixConfiguration, Matrix


class ScreenMatrix(Matrix):
    def __init__(self, config:MatrixConfiguration):
        super().__init__(config)
        self.__options = RGBMatrixOptions()

        # figure out how many panels in rows / cols
        self.__panel_rows = config.overall_led_height / config.panel_led_height
        self.__panel_cols = config.overall_led_width / config.panel_led_width
        self.__options.chain_length = self.__panel_cols * self.__panel_rows

        self.__options.rows = config.panel_led_height
        self.__options.cols = config.panel_led_width
        self.__options.parallel = 1
        self.__options.hardware_mapping = config.hardware_mapping
        self.__options.gpio_slowdown = config.gpio_slowdown
        self.__options.limit_refresh_rate_hz = config.limit_refresh_rate_hz
        self.__options.brightness = config.brightness
        self.__options.disable_hardware_pulsing = config.disable_hardware_pulsing
        self.__options.drop_privileges = config.drop_privileges
        self.__matrix = RGBMatrix(options=self.__options)
        self.__next_canvas = None

    def start_new_canvas(self):
        self.__next_canvas = self.__matrix.CreateFrameCanvas()

    def finish_canvas(self):
        self.__matrix.SwapOnVSync(self.__next_canvas)
        self.__next_canvas = None

    def render_image(self, image: Image):
        if self.__panel_rows > 1:
            # rearrange for rendering...
            top_half = image.crop((0, 0, self.config.overall_led_width, self.config.panel_led_height))
            bottom_half = image.crop((0, self.config.panel_led_height, self.config.overall_led_width, self.config.overall_led_height))

            stitched = Image.new('RGB', (self.config.overall_led_width * 2, self.config.panel_led_height))
            stitched.paste(top_half, (0, 0))
            stitched.paste(bottom_half, (self.config.overall_led_width, 0))

            rgb = stitched.convert('RGB')
        else:
            rgb = image.convert('RGB')

        if self.__next_canvas is not None:
            self.__next_canvas.SetImage(rgb)
        else:
            canvas = self.__matrix.CreateFrameCanvas()
            canvas.SetImage(rgb)
            self.__matrix.SwapOnVSync(canvas)

    def set_pixel(self, x, y, r, g, b):
        t_x = x
        t_y = y
        if self.__panel_rows > 1:
            if t_y >= self.config.panel_led_height:
                t_x = t_x + self.config.overall_led_width
                t_y = t_y - self.config.panel_led_height
        if self.__next_canvas is not None:
            self.__next_canvas.SetPixel(t_x, t_y, r, g, b)
        else:
            self.__matrix.SetPixel(t_x, t_y, r, g, b)

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
