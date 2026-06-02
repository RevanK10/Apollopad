import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler

# ----------------------------
# Keyboard object
# ----------------------------
keyboard = KMKKeyboard()

# ----------------------------
# Keys (5 switches + encoder button)
# ----------------------------
# Update these to match the actual GPIO numbers for the XIAO RP2040
PINS = [
    board.GP26,  # SW1 (Pin 1 / C1)
    board.GP28,  # SW2 (Pin 3 / C3)
    board.GP27,  # SW3 (Pin 2 / C2)
    board.GP29,  # SW4 (Pin 4 / SCLK) - Check if this is SW4 or SW5 on your board
    board.GP6,   # SW5 (Pin 5 / SDA)
    board.GP0,   # Encoder push (Pin 8 / RX)
]

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
    pull=True, # Ensure internal pull-ups are enabled
)

# ... inside EncoderHandler ...


# ----------------------------
# Rotary encoder
# ----------------------------
encoder = EncoderHandler()
keyboard.modules.append(encoder)

encoder.pins = (
    (board.GP3, board.GP2),  # A=Pin 11 (D1), B=Pin 10 (D2)
)

# ----------------------------
# Keymap
# ----------------------------
keyboard.keymap = [
    [
        KC.MUTE,        # SW1
        KC.VOLDOWN,     # SW2
        KC.VOLUP,       # SW3
        KC.PLAY_PAUSE,  # SW4
        KC.ENTER,       # SW5
        KC.MUTE,        # Encoder button
    ]
]

encoder.map = [
    (
        KC.VOLDOWN,  # Rotate left
        KC.VOLUP,    # Rotate right
    )
]

# ----------------------------
# Start KMK
# ----------------------------
if __name__ == '__main__':
    keyboard.go()

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
