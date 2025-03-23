import dearpygui.dearpygui as dpg

from pipypixels.controls.shared import Command
from pipypixels.graphics.local import FakeMatrix
from pipypixels.screens import ScreenController


class UICommandSource:
    def __init__(self, screen_controller: ScreenController, matrix:FakeMatrix):
        self.__screen_controller = screen_controller
        self.__matrix = matrix

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

    def __frame_rate_up(self):
        self.__screen_controller.receive_command(Command.FRAME_RATE_UP)

    def __frame_rate_down(self):
        self.__screen_controller.receive_command(Command.FRAME_RATE_DOWN)

    def __reset(self):
        self.__screen_controller.receive_command(Command.RESET)

    def __screenshot(self):
        dpg.show_item('file_dialog')

    def __screenshot_save(self, sender, app_data):
        self.__matrix.save_matrix_as_image(app_data['file_path_name'] + '.png')

    def __preset_1(self, sender, app_data):
        self.__screen_controller.receive_command(Command.PRESET_1)

    def __preset_2(self, sender, app_data):
        self.__screen_controller.receive_command(Command.PRESET_2)

    def __preset_3(self, sender, app_data):
        self.__screen_controller.receive_command(Command.PRESET_3)

    def __preset_4(self, sender, app_data):
        self.__screen_controller.receive_command(Command.PRESET_4)

    def __preset_5(self, sender, app_data):
        self.__screen_controller.receive_command(Command.PRESET_5)

    def __preset_6(self, sender, app_data):
        self.__screen_controller.receive_command(Command.PRESET_6)

    def __preset_7(self, sender, app_data):
        self.__screen_controller.receive_command(Command.PRESET_7)

    def __preset_8(self, sender, app_data):
        self.__screen_controller.receive_command(Command.PRESET_8)

    def __preset_9(self, sender, app_data):
        self.__screen_controller.receive_command(Command.PRESET_9)

    def __preset_10(self, sender, app_data):
        self.__screen_controller.receive_command(Command.PRESET_10)

    def create_buttons(self):
        dpg.add_file_dialog(tag='file_dialog', show=False, callback=self.__screenshot_save, width=600, height=400)
        with dpg.table(header_row=False):
            dpg.add_table_column()

            with dpg.table_row():
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
                            dpg.add_button(label='Frame Rate Up', callback=self.__frame_rate_up)
                            dpg.add_button(label='Frame Rate Down', callback=self.__frame_rate_down)
                        with dpg.table_row():
                            dpg.add_button(label='Preset 1', callback=self.__preset_1)
                            dpg.add_button(label='Preset 2', callback=self.__preset_2)
                        with dpg.table_row():
                            dpg.add_button(label='Preset 3', callback=self.__preset_3)
                            dpg.add_button(label='Preset 4', callback=self.__preset_4)
                        with dpg.table_row():
                            dpg.add_button(label='Preset 5', callback=self.__preset_5)
                            dpg.add_button(label='Preset 6', callback=self.__preset_6)
                        with dpg.table_row():
                            dpg.add_button(label='Preset 7', callback=self.__preset_7)
                            dpg.add_button(label='Preset 8', callback=self.__preset_8)
                        with dpg.table_row():
                            dpg.add_button(label='Preset 9', callback=self.__preset_9)
                            dpg.add_button(label='Preset 10', callback=self.__preset_10)
            with dpg.table_row():
                with dpg.collapsing_header(label='Local Controls', default_open=True):
                    with dpg.table(header_row=False):
                        dpg.add_table_column()
                        with dpg.table_row():
                            dpg.add_button(label='Screenshot', callback=self.__screenshot)
