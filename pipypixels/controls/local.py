import dearpygui.dearpygui as dpg

from pipypixels.controls.shared import Command
from pipypixels.screens import ScreenController


class UICommandSource:
    def __init__(self, screen_controller: ScreenController):
        self.__screen_controller = screen_controller

    def __pause_play(self):
        self.__screen_controller.receive_command(Command.PAUSE_PLAY)

    def __power(self):
        self.__screen_controller.receive_command(Command.POWER)

    def __previous(self):
        self.__screen_controller.receive_command(Command.PREVIOUS)

    def __next(self):
        self.__screen_controller.receive_command(Command.NEXT)

    def __step_forward(self):
        self.__screen_controller.receive_command(Command.STEP_FORWARD)

    def __step_back(self):
        self.__screen_controller.receive_command(Command.STEP_BACKWARD)

    def __zoom_in(self):
        self.__screen_controller.receive_command(Command.ZOOM_IN)

    def __zoom_out(self):
        self.__screen_controller.receive_command(Command.ZOOM_OUT)

    def __brightness_up(self):
        self.__screen_controller.receive_command(Command.BRIGHTNESS_UP)

    def __brightness_down(self):
        self.__screen_controller.receive_command(Command.BRIGHTNESS_DOWN)

    def __framerate_up(self):
        self.__screen_controller.receive_command(Command.FRAMERATE_UP)

    def __framerate_down(self):
        self.__screen_controller.receive_command(Command.FRAMERATE_DOWN)

    def __reset(self):
        self.__screen_controller.receive_command(Command.RESET)

    def create_buttons(self):
        with dpg.collapsing_header(label='Remote Controls', default_open=True):
            with dpg.table(header_row=False):
                dpg.add_table_column()
                dpg.add_table_column()
                with dpg.table_row():
                    dpg.add_button(label='Power', callback=self.__power)
                    dpg.add_button(label='Reset', callback=self.__reset)
                with dpg.table_row():
                    dpg.add_button(label='Pause / Play', callback=self.__pause_play)
                with dpg.table_row():
                    dpg.add_button(label='Step Back', callback=self.__step_back)
                    dpg.add_button(label='Step Forward', callback=self.__step_forward)
                with dpg.table_row():
                    dpg.add_button(label='Prev', callback=self.__previous)
                    dpg.add_button(label='Next', callback=self.__next)
                with dpg.table_row():
                    dpg.add_button(label='Zoom In', callback=self.__zoom_in)
                    dpg.add_button(label='Zoom Out', callback=self.__zoom_out)
                with dpg.table_row():
                    dpg.add_button(label='Brightness Up', callback=self.__brightness_up)
                    dpg.add_button(label='Brightness Down', callback=self.__brightness_down)
                with dpg.table_row():
                    dpg.add_button(label='Framerate Up', callback=self.__framerate_up)
                    dpg.add_button(label='Framerate Down', callback=self.__framerate_down)