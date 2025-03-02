from PIL import Image
from numpy import asarray
import dearpygui.dearpygui as dpg

from pipypixels.graphics.shared import ScreenMatrixConfiguration


class FakeMatrix:
    def __init__(self, config:ScreenMatrixConfiguration):
        self.config = config
        self.__led_size = 5

        panel_width = config.overall_led_cols * self.__led_size
        panel_height = config.overall_led_rows * self.__led_size

        dpg.add_drawlist(width=panel_width, height=panel_height, tag='LED_PANEL')

        self.__create_pixels()

    def start_new_canvas(self):
        pass

    def finish_canvas(self):
        pass

    def clear(self):
        pass

    def set_pixel(self, x, y, r, g, b):
        tag = 'pixel_' + str(x) + '_' + str(y)
        dpg.configure_item(tag, fill=(r,g,b))

    def __create_pixels(self):
        for x in range(self.config.overall_led_cols):
            for y in range(self.config.overall_led_rows):
                t_x = x * self.__led_size
                t_y = y * self.__led_size
                p_min = (t_x, t_y)
                p_max = (t_x + self.__led_size, t_y + self.__led_size)
                tag = 'pixel_' + str(x) + '_' + str(y)
                dpg.draw_rectangle(p_min, p_max, color=(0, 0, 0), thickness=0, fill=(0,0,0), parent='LED_PANEL', tag=tag)

    def render_image(self, image: Image):
        data = asarray(image)
        for y in range(len(data)):
            row = data[y]
            for x in range(len(row)):
                rgb = row[x]
                self.set_pixel(x, y, rgb[0], rgb[1], rgb[2])
