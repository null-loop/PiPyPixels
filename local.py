import dearpygui.dearpygui as dpg

from pipypixels.games.life import GameOfLifeEngine
from pipypixels.graphics.config import ScreenMatrixConfiguration
from pipypixels.graphics.fakematrix import FakeMatrix

def pause_play():
    life.toggle_pause()

config = ScreenMatrixConfiguration()

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
            life = GameOfLifeEngine(1, matrix, 24)
            life.random_spawn(5)

dpg.create_viewport(title='PiPyPixels Local Debug Environment', width=900)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Matrix", True)
try:
    life.begin()
    dpg.start_dearpygui()
finally:
    life.end()
    dpg.destroy_context()
