from PIL import Image


class MatrixConfiguration:
    panel_led_height = 64
    panel_led_width = 64
    overall_led_height = 128
    overall_led_width = 128
    hardware_mapping = 'adafruit-hat-pwm'
    limit_refresh_rate_hz = 120
    brightness = 50
    disable_hardware_pulsing = False
    drop_privileges = False

class Matrix:
    def __init__(self, config:MatrixConfiguration):
        self.config = config

    def start_new_canvas(self):
        pass

    def finish_canvas(self):
        pass

    def render_image(self, image: Image):
        pass

    def set_pixel(self, x, y, r, g, b):
        pass

    def clear(self):
        pass

    def increase_brightness(self):
        pass

    def decrease_brightness(self):
        pass