# Import board pin definitions
import board

# KMK core
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC

# Encoder support
from kmk.modules.encoder import EncoderHandler

# Create keyboard object
keyboard = KMKKeyboard()

# ========== KEYS ==========
# Order MUST match PCB wiring order

PINS = [
    board.A0,  # SW1 - Copy
    board.A1,  # SW2 - Paste
    board.A2,  # SW3 - Cut
    board.A3,  # SW4 - Play / Pause
    board.D6,  # SW5 - Screenshot
    board.D7,  # Encoder press (Mute)
]

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

# ========== ROTARY ENCODER ==========
encoder = EncoderHandler()
keyboard.modules.append(encoder)

encoder.pins = (
    (board.D2, board.D1),  # Encoder A, B
)

encoder.map = [
    (
        KC.VOLDOWN,  # Rotate left
        KC.VOLUP,    # Rotate right
    )
]

# ========== KEYMAP ==========
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

if __name__ == '__main__':
    keyboard.go()
