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
PINS = [
    board.A0,  # SW1
    board.A1,  # SW2
    board.A2,  # SW3
    board.A3,  # SW4
    board.D6,  # SW5
    board.D7,  # Encoder push
]

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,  # internal pull-ups
)

# ----------------------------
# Rotary encoder
# ----------------------------
encoder = EncoderHandler()
keyboard.modules.append(encoder)

encoder.pins = (
    (board.D1, board.D2),  # A, B
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
