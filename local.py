import dearpygui.dearpygui as dpg

from pipypixels.controls.local import UICommandSource
from pipypixels.controls.shared import Command
from pipypixels.graphics.local import FakeMatrix
from pipypixels.graphics.shared import MatrixConfiguration
from pipypixels.screens import ScreenController
from pipypixels.shared import load_config, load_screens


def __exit_app():
    dpg.stop_dearpygui()

all_config = load_config()
matrix = FakeMatrix(MatrixConfiguration.create_from_json(all_config))
controller = ScreenController(matrix)

load_screens(all_config, controller, matrix)

command_source = UICommandSource(controller, matrix)

dpg.create_context()

with dpg.window(tag="Matrix"):
    with dpg.menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Exit", callback=__exit_app)
    with dpg.table(header_row=False):
        dpg.add_table_column(width=matrix.panel_width, width_fixed=True)
        dpg.add_table_column()
        with dpg.table_row():
            matrix.create_led_panel()
            command_source.create_buttons()

dpg.create_viewport(title='PiPyPixels Local Debug Environment', width=matrix.panel_width + 250)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Matrix", True)
try:
    matrix.create_pixels()
    controller.begin()
    dpg.start_dearpygui()
finally:
    controller.receive_command(Command.EXIT)
    dpg.destroy_context()
