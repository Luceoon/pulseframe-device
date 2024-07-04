import time
import board
import gifio
import displayio
import state
import api
import anim

from adafruit_matrixportal.network import Network

import adafruit_requests as requests

last_timestamp = 0
anim_duration = 20

anim.load_and_play("pulseframe_loading.gif")

# --- Network setup ---


try:
    from secrets import secrets
except ImportError:
    print('WiFi secrets are kept in secrets.py, please add them there!')
    raise

NETWORK = Network(status_neopixel=board.NEOPIXEL, debug=False)

try:
    NETWORK.connect()
except RuntimeError as e:
    try: 
        print("Some error occured, retrying! -", e)
        time.sleep(3)
        NETWORK.connect()
    except RuntimeError as e:
        print("Couldn't connect to network!! -", e)
        raise

print ("Connected to Network! My IP is: ", NETWORK.ip_address)


state.init()


current_animation_index = 0
#anim.load_and_play(state.getAnimations()[current_animation_index])

print("Ready Looping...")

while True:
    state.tick()
    anim.tick()

    if time.monotonic() - last_timestamp > anim_duration:
        current_animation_index += 1
        if current_animation_index >= len(state.getAnimations()):
            current_animation_index = 0
        entry = state.getAnimations()[current_animation_index]
        anim.load_and_play(entry[0])
        anim_duration = entry[1]
        last_timestamp = time.monotonic()