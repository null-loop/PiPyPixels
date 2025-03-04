from PIL import Image
from numpy import asarray
import dearpygui.dearpygui as dpg

from pipypixels.graphics.shared import MatrixConfiguration, Matrix


class FakeMatrix(Matrix):
    def __init__(self, config: MatrixConfiguration):
        super().__init__(config)
        self.__led_size = 5
        self.__brightness = config.brightness

        self.panel_width = config.overall_led_cols * self.__led_size
        self.panel_height = config.overall_led_rows * self.__led_size

        self.__created_pixels = False

    def start_new_canvas(self):
        self.__ensure_pixels_created()

    def finish_canvas(self):
        self.__ensure_pixels_created()

    def clear(self):
        self.__ensure_pixels_created()
        for x in range(self.config.overall_led_cols):
            for y in range(self.config.overall_led_rows):
                self.set_pixel(x,y,0,0,0)

    def __ensure_pixels_created(self):
        if not self.__created_pixels:
            self.create_pixels()

    def set_pixel(self, x, y, r, g, b):
        self.__ensure_pixels_created()
        tag = 'pixel_' + str(x) + '_' + str(y)
        dpg.configure_item(tag, fill=(r,g,b,int(255*self.__brightness/100)))

    def create_pixels(self):
        self.__created_pixels = True
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

    def increase_brightness(self):
        old = self.__brightness
        self.__brightness = min(self.__brightness + 10, 100)
        return old != self.__brightness

    def decrease_brightness(self):
        old = self.__brightness
        self.__brightness = max(self.__brightness - 10, 1)
        return old != self.__brightness

    def create_led_panel(self):
        dpg.add_drawlist(width=self.panel_width, height=self.panel_height, tag='LED_PANEL')
