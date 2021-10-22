import time
from keyboard import Wormier_K66

with Wormier_K66() as kb:
    # Clear colours for all keys
    with kb.transaction():
        for i in range(0, 122, 18):
            kb.raw_key_rgb(i, [0] * 18)

    # Put mode to custom RGB values (Coastal)
    with kb.transaction():
        kb.set_brightness(3)
        kb.set_mode(20)

    # Blink it twice
    for _ in range(2):
        with kb.transaction():
            kb.raw_key_rgb(22, [0xff00ff, 0x00ff00, 0x0000ff, 0xffff00])
        time.sleep(1)

        with kb.transaction():
            kb.raw_key_rgb(22, [0, 0, 0, 0])
        time.sleep(1)

    with kb.transaction():
        kb.set_mode(1)
        kb.set_brightness(2)

