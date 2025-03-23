import dearpygui.dearpygui as dpg

from pipypixels.controls.shared import Command
from pipypixels.games.bounce import BounceScreen
from pipypixels.games.life import GameOfLifeScreen
from pipypixels.games.maze import MazeScreen
from pipypixels.games.snakes import SnakeScreen
from pipypixels.graphics.local import FakeMatrix
from pipypixels.graphics.shared import MatrixConfiguration
from pipypixels.screens import ScreenController, StartupImageScreen, ArtImageScreen
from pipypixels.controls.local import UICommandSource

def __exit_app():
    dpg.stop_dearpygui()

config = MatrixConfiguration.load('config/config.json')
matrix = FakeMatrix(config)
controller = ScreenController(matrix)
controller.add_screen(StartupImageScreen(matrix))
controller.add_screen(ArtImageScreen(matrix))
controller.add_screen(BounceScreen(matrix))
controller.add_screen(SnakeScreen(matrix))
controller.add_screen(MazeScreen(matrix))
controller.add_screen(GameOfLifeScreen(matrix))
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
