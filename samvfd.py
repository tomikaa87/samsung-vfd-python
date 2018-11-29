import serial
import time


CMD_RESET = 0x1f
CMD_SET_DIM_LEVEL = 0x04
CMD_SET_POSITION = 0x10
CMD_DEFINE_CHAR = 0x1b

DISPLAY_MODE_NORMAL, DISPLAY_MODE_V_SCROLL, DISPLAY_MODE_H_SCROLL = (0x11, 0x12, 0x16)
CURSOR_ON, CURSOR_OFF, CURSOR_BLINK = (0x13, 0x14, 0x15)
DIM_LEVEL_20, DIM_LEVEL_40, DIM_LEVEL_60, DIM_LEVEL_100 = (0, 0x40, 0x60, 0x80)
FONT_GENERAL_EU, FONT_JAPANESE_KATAKANA = (0x18, 0x19)


class SamVfd:
    _port = None
    _serial = None
    _debug_log = False

    def __init__(self, port, baud_rate=9600, debug_log=False):
        self._debug_log = debug_log
        self._port = port
        self._serial = serial.Serial(port, stopbits=serial.STOPBITS_TWO, baudrate=baud_rate)

    def __del__(self):
        if self._serial.is_open:
            self.__debug_log("closing port %s" % self._port)
            self._serial.close()

    def open(self):
        if self._serial.is_open:
            self._serial.close()

        self.__debug_log("open: port=%s" % self._port)
        self._serial.open()

        if not self._serial.is_open:
            self.__debug_log("open: port cannot be opened")
            exit(1)

    def reset(self):
        self.__debug_log("reset")
        self.send_command(CMD_RESET)
        time.sleep(0.01)

    def set_cursor(self, mode):
        self.__debug_log("set_cursor: %d" % mode)
        if mode not in (CURSOR_ON, CURSOR_OFF, CURSOR_BLINK):
            self.__debug_log("set_cursor: invalid mode")
            return
        self.send_command(mode)

    def set_dim_level(self, level):
        self.__debug_log("set_dim_level: %d" % level)
        if level not in (DIM_LEVEL_20, DIM_LEVEL_40, DIM_LEVEL_60, DIM_LEVEL_100):
            self.__debug_log("set_dim_level: invalid level")
            return
        self.send_command(CMD_SET_DIM_LEVEL)
        self.send_command(level)

    def set_display_mode(self, mode):
        self.__debug_log("set_display_mode: %d" % mode)
        if mode not in (DISPLAY_MODE_NORMAL, DISPLAY_MODE_V_SCROLL, DISPLAY_MODE_H_SCROLL):
            self.__debug_log("set_display_mode: invalid mode")
            return
        self.send_command(mode)

    def set_position(self, col, row):
        self.__debug_log("set_position: col=%d, row=%d" % (col, row))
        pos = row * 20 + col
        if -1 < pos < 40:
            self.send_command(CMD_SET_POSITION)
            self.send_command(pos)
        else:
            self.__debug_log("set_position: invalid position")

    def set_font(self, font):
        self.__debug_log("set_font: %d" % font)
        if font not in (FONT_GENERAL_EU, FONT_JAPANESE_KATAKANA):
            self.__debug_log("set_font: invalid font")
            return
        self.send_command(font)

    def define_char(self, position, data):
        self.__debug_log("define_char: position=%d, data_len=%d" % (position, len(data)))
        if position < 0 or position > 4 or len(data) != 5:
            self.__debug_log("define_char: invalid parameter(s)")
            return
        self.send_command(CMD_DEFINE_CHAR)
        self.send_command(position)
        self.send(data)

    def send_command(self, command):
        if not isinstance(command, int):
            self.__debug_log("send_command error: command must be an integer")
            return

        self.__debug_log("send_command: 0x%02X" % command)

        written = self._serial.write([command])
        if written != 1:
            self.__debug_log("send_command error: written bytes: %d" % written)

    def send(self, data):
        written = self._serial.write(data)
        self.__debug_log("send: data_len=%d, written=%d, data=%s"
                         % (len(data),
                            written,
                            "".join(["0x%02X " % ord(x) for x in data]).strip()))
        if len(data) != written:
            self.__debug_log("send error: written bytes != data length (%d != %d)" % (written, len(data)))

    def __debug_log(self, log):
        if self._debug_log:
            print("SamVFD: %s" % log)
