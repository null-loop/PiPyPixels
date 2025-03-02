import dearpygui.dearpygui as dpg
from PIL import Image

from pipypixels.graphics.fakematrix import FakeMatrix
from pipypixels.graphics.options import ScreenMatrixConfiguration

dpg.create_context()

with dpg.window(tag="Matrix"):
    config = ScreenMatrixConfiguration()
    matrix = FakeMatrix(config)
    matrix.render_image(Image.open("../assets/led.png"))

dpg.create_viewport(title='PiPyPixels Local Debug Environment', width=1000, height=1000)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Matrix", True)
dpg.start_dearpygui()
dpg.destroy_context()