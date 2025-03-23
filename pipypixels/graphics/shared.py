import json
import string

from PIL import Image


class MatrixConfiguration:
    panel_led_height = 64
    panel_led_width = 64
    overall_led_height = 64
    overall_led_width = 64
    hardware_mapping = 'adafruit-hat-pwm'
    gpio_slowdown = 5
    limit_refresh_rate_hz = 0
    brightness = 50
    disable_hardware_pulsing = False
    drop_privileges = False

    @staticmethod
    def load(file_path:string):
        with open(file_path) as json_data:
            config = json.load(json_data)
            matrix_config = MatrixConfiguration()

            matrix_config.panel_led_width = config['matrix']['panel_led_width']
            matrix_config.panel_led_height = config['matrix']['panel_led_height']

            matrix_config.overall_led_width = config['matrix']['overall_led_width']
            matrix_config.overall_led_height = config['matrix']['overall_led_height']

            matrix_config.hardware_mapping = config['matrix']['hardware_mapping']
            matrix_config.gpio_slowdown = config['matrix']['gpio_slowdown']
            matrix_config.limit_refresh_rate_hz = config['matrix']['limit_refresh_rate_hz']
            matrix_config.brightness = config['matrix']['brightness']
            matrix_config.disable_hardware_pulsing = config['matrix']['disable_hardware_pulsing']
            matrix_config.drop_privileges = config['matrix']['drop_privileges']
            return matrix_config

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