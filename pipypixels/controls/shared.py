from enum import Enum


class Command(Enum):
    NONE = -1
    RESET = 0
    POWER = 1
    STEP_BACKWARD = 2
    STEP_FORWARD = 3
    PREVIOUS = 4
    NEXT = 5
    PAUSE_PLAY = 6
    BRIGHTNESS_UP = 7
    BRIGHTNESS_DOWN = 8
    FRAME_RATE_UP = 9
    FRAME_RATE_DOWN = 10
    ZOOM_IN = 11
    ZOOM_OUT = 12
    PAUSE = 13
    PLAY = 14
    PRESET_1 = 100
    PRESET_2 = 101
    PRESET_3 = 102
    PRESET_4 = 103
    PRESET_5 = 104
    PRESET_6 = 105
    PRESET_7 = 106
    PRESET_8 = 107
    PRESET_9 = 108
    PRESET_0 = 109
    NEXT_AND_REMOVE = 200
    PREV_AND_REMOVE = 201
    EXIT = 999