import gifio
import displayio

class PulseGIF:
    def __init__(self, gif_path):
        self.gif_path = gif_path
        self.gif = None
        self.bitmap = None
        self.palette = None
        self.tile_grid = None
        self.overhead = None
        self.next_delay = None
        self.load_gif()
        self.next_frame()
        self.get_tile_grid()
        self.get_bitmap()
        self.get_palette()
        self.get_gif()
    
    def load_gif(self):
        # Load the GIF into memory
        print("Loading GIF...")
        self.gif = gifio.Gif(self.gif_path)
        print("GIF loaded!")

        start = time.monotonic()
        self.next_delay = self.gif.next_frame() # Load the first frame
        end = time.monotonic()
        self.overhead = end - start

        # Create a bitmap and palette for the GIF
        self.bitmap = displayio.Bitmap(self.gif.width, self.gif.height, self.gif.palette.size)
        self.palette = displayio.Palette(self.gif.palette.size)
        # Copy the palette into the displayio palette
        for i in range(self.palette.size):
            self.palette[i] = self.gif.palette[i]
        # Create a TileGrid using the Bitmap and Palette
        self.tile_grid = displayio.TileGrid(self.bitmap, pixel_shader=self.palette)
        return self.tile_grid, self.bitmap, self.palette, self.gif

    def next_frame(self):
        # Load the next frame into the bitmap
        self.bitmap, self.palette = self.gif.get_next_frame(self.bitmap, self.palette)
        # Return the delay for the frame
        return self.gif.frame_delay

    def get_tile_grid(self):
        return self.tile_grid

    def get_bitmap(self):
        return self.bitmap

    def get_palette(self):
        return self.palette

    def get_gif(self):
        return self.gif


