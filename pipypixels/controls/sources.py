import dearpygui.dearpygui as dpg
import keyboard

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
        with dpg.table(header_row=False):
            dpg.add_table_column()
            dpg.add_table_column()
            with dpg.table_row():
                dpg.add_button(label='Power', callback=self.__power)
                dpg.add_button(label='Reset', callback=self.__reset)
            with dpg.table_row():
                dpg.add_button(label='Pause / Play', callback=self.__pause_play)
                dpg.add_button(label='Step Fwd', callback=self.__step_forward)
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

class RemoteKeyboardCommandSource:
    def __init__(self, screen_controller: ScreenController):
        self.__screen_controller = screen_controller
        keyboard.on_press(lambda key_event: self.__key_pressed(key_event.scan_code, key_event.name))

    def __key_pressed(self, scan_code, name):
        command = Command.NONE
        if scan_code == 116: command = Command.POWER
        elif scan_code == 168: command = Command.STEP_BACKWARD
        elif scan_code == 208: command = Command.STEP_FORWARD
        elif scan_code == 165: command = Command.PREVIOUS
        elif scan_code == 163: command = Command.NEXT
        elif scan_code == 164: command = Command.PAUSE_PLAY
        elif scan_code == 2: command = Command.PRESET_1
        elif scan_code == 3: command = Command.PRESET_2
        elif scan_code == 4: command = Command.PRESET_3
        elif scan_code == 5: command = Command.PRESET_4
        elif scan_code == 6: command = Command.PRESET_5
        elif scan_code == 7: command = Command.PRESET_6
        elif scan_code == 8: command = Command.PRESET_7
        elif scan_code == 9: command = Command.PRESET_8
        elif scan_code == 10: command = Command.PRESET_9
        elif scan_code == 11: command = Command.PRESET_10
        elif scan_code == 113: command = Command.RESET
        elif scan_code == 115: command = Command.BRIGHTNESS_UP
        elif scan_code == 114: command = Command.BRIGHTNESS_DOWN
        elif scan_code == 104: command = Command.FRAMERATE_UP
        elif scan_code == 109: command = Command.FRAMERATE_DOWN
        elif scan_code == 418: command = Command.ZOOM_IN
        elif scan_code == 419: command = Command.ZOOM_OUT

        if command != Command.NONE:
            self.__screen_controller.receive_command(command)