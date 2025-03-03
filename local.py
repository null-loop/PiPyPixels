import dearpygui.dearpygui as dpg

from pipypixels.controls.shared import Command
from pipypixels.games.life import GameOfLifeScreen
from pipypixels.graphics.fakematrix import FakeMatrix
from pipypixels.graphics.shared import MatrixConfiguration
from pipypixels.screens import ScreenController, StartupImageScreen
from pipypixels.controls.local import UICommandSource

config = MatrixConfiguration()
config.brightness = 100

dpg.create_context()

with dpg.window(tag="Matrix"):
    with dpg.table(header_row=False):
        dpg.add_table_column(width_fixed=True, width=800)
        dpg.add_table_column()

        with dpg.table_row():
            matrix = FakeMatrix(config)
            controller = ScreenController()
            controller.add_screen(GameOfLifeScreen(matrix))
            controller.add_screen(StartupImageScreen(matrix))
            command_source = UICommandSource(controller)
            command_source.create_buttons()

dpg.create_viewport(title='PiPyPixels Local Debug Environment', width=900)

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
