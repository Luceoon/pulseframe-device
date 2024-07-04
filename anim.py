import gifio
import time
import displayio

from adafruit_matrixportal.matrix import Matrix


matrix = Matrix()
display = matrix.display

current_gif = None
overhead = 0
next_delay = 0
last_frame = 0

anim_group = displayio.Group()

def load_and_play(file):
    global current_gif, overhead, next_delay
    
    if len(anim_group) > 0:
        anim_group.pop()
    
    if current_gif:
        current_gif.deinit()

    current_gif = gifio.OnDiskGif("/data/" + file)
    start = time.monotonic()
    next_delay = current_gif.next_frame() # Load the first frame
    end = time.monotonic()
    overhead = end - start

    # --- Drawing setup ---


    face = displayio.TileGrid(
        current_gif.bitmap,
        pixel_shader=displayio.ColorConverter(
            input_colorspace=displayio.Colorspace.RGB565_SWAPPED
        ),
    )
    anim_group.append(face)
    display.show(anim_group)
    display.refresh()

def next_frame():
    global next_delay
    next_delay = current_gif.next_frame() # Load the next frame
    
def tick():
    global last_frame, next_delay, overhead
    if time.monotonic() - last_frame > next_delay - overhead:
        next_frame()
        last_frame = time.monotonic()