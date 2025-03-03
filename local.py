import dearpygui.dearpygui as dpg

from pipypixels.controls import Command
from pipypixels.games.life import GameOfLifeScreen
from pipypixels.graphics.fakematrix import FakeMatrix
from pipypixels.graphics.shared import MatrixConfiguration
from pipypixels.screens import ScreenController


def pause_play():
    controller.receive_command(Command.PAUSE_PLAY)

config = MatrixConfiguration()

dpg.create_context()

with dpg.window(tag="Matrix"):
    with dpg.table(header_row=False):
        dpg.add_table_column(width_fixed=True, width=800)
        dpg.add_table_column()

        with dpg.table_row():
            matrix = FakeMatrix(config)
            with dpg.table(header_row=False):
                dpg.add_table_column()
                with dpg.table_row():
                    dpg.add_button(label='Pause/Play', callback=pause_play)

            controller = ScreenController()
            controller.add_screen(GameOfLifeScreen(matrix))

dpg.create_viewport(title='PiPyPixels Local Debug Environment', width=900)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Matrix", True)
try:
    controller.begin()
    dpg.start_dearpygui()
finally:
    dpg.destroy_context()
