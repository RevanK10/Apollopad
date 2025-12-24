# =========================
# Imports
# =========================

import board
import busio
import displayio
import terminalio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler

from adafruit_display_text import label
from adafruit_ssd1306 import SSD1306_I2C


# =========================
# Keyboard setup
# =========================

keyboard = KMKKeyboard()

PINS = [
    board.A0,  # SW1 - Copy
    board.A1,  # SW2 - Paste
    board.A2,  # SW3 - Cut
    board.A3,  # SW4 - Play / Pause
    board.D6,  # SW5 - Screenshot
    board.D7,  # Encoder press - Mute
]

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

# =========================
# Encoder setup
# =========================

encoder = EncoderHandler()
keyboard.modules.append(encoder)

encoder.pins = (
    (board.D2, board.D1),  # Encoder A, B
)

# Local volume tracker (0–100)
volume = 50

def update_oled():
    volume_label.text = f"Volume: {volume}%"

def volume_down(keyboard):
    global volume
    volume = max(0, volume - 5)
    update_oled()
    return KC.VOLDOWN

def volume_up(keyboard):
    global volume
    volume = min(100, volume + 5)
    update_oled()
    return KC.VOLUP

encoder.map = [
    (volume_down, volume_up)
]

# =========================
# OLED setup
# =========================

displayio.release_displays()

i2c = busio.I2C(board.SCL, board.SDA)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = SSD1306_I2C(128, 32, display_bus)

group = displayio.Group()
display.show(group)

volume_label = label.Label(
    terminalio.FONT,
    text="Volume: 50%",
    x=0,
    y=15,
)

group.append(volume_label)

# =========================
# Keymap
# =========================

keyboard.keymap = [
    [
        KC.COPY,        # SW1
        KC.PASTE,       # SW2
        KC.CUT,         # SW3
        KC.PLAY_PAUSE,  # SW4
        KC.SCREENSHOT,  # SW5
        KC.MUTE,        # Encoder press
    ]
]

# =========================
# Start KMK
# =========================

if __name__ == "__main__":
    keyboard.go()
