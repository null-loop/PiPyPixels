from PIL import Image, ImageDraw
from numpy import asarray
import dearpygui.dearpygui as dpg

from pipypixels.graphics.shared import MatrixConfiguration, Matrix


class FakeMatrix(Matrix):
    def __init__(self, config: MatrixConfiguration):
        super().__init__(config)
        self.__led_size = 5
        self.__brightness = config.brightness

        self.panel_width = config.overall_led_width * self.__led_size
        self.panel_height = config.overall_led_height * self.__led_size

        self.__created_pixels = False
        self.__pixels = []

    def start_new_canvas(self):
        self.__ensure_pixels_created()

    def finish_canvas(self):
        self.__ensure_pixels_created()

    def clear(self):
        self.__ensure_pixels_created()
        for x in range(self.config.overall_led_width):
            for y in range(self.config.overall_led_height):
                self.set_pixel(x,y,0,0,0)

    def __ensure_pixels_created(self):
        if not self.__created_pixels:
            self.create_pixels()

    def set_pixel(self, x, y, r, g, b):
        self.__ensure_pixels_created()
        tag = 'pixel_' + str(x) + '_' + str(y)
        dpg.configure_item(tag, fill=(r,g,b,int(255*self.__brightness/100)))
        self.__pixels[x][y] = (r,g,b)

    def save_matrix_as_image(self, file_path):
        pixel_size = 6
        image = Image.new('RGB', (self.config.overall_led_width * pixel_size, self.config.overall_led_height * pixel_size))
        draw = ImageDraw.Draw(image)
        for x in range(self.config.overall_led_width):
            for y in range(self.config.overall_led_height):
                t_x = x * pixel_size
                t_y = y * pixel_size
                draw.rectangle((t_x,t_y,t_x + pixel_size,t_y + pixel_size),fill=(0,0,0))
                colour = self.__pixels[x][y]
                safe_colour = (int(colour[0]),int(colour[1]),int(colour[2]))
                draw.rectangle((t_x + 1, t_y + 1, t_x + pixel_size - 2, t_y + pixel_size - 2), fill=safe_colour)
        image.save(file_path, 'png')

    def create_pixels(self):
        self.__created_pixels = True
        for x in range(self.config.overall_led_width):
            col = []
            self.__pixels.append(col)
            for y in range(self.config.overall_led_height):
                t_x = x * self.__led_size
                t_y = y * self.__led_size
                p_min = (t_x, t_y)
                p_max = (t_x + self.__led_size, t_y + self.__led_size)
                tag = 'pixel_' + str(x) + '_' + str(y)
                dpg.draw_rectangle(p_min, p_max, color=(0, 0, 0), thickness=0, fill=(0,0,0), parent='LED_PANEL', tag=tag)
                col.append((0,0,0))

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
