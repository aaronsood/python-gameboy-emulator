import sys
import os

# add parent folder to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rom import ROM
from memory import Memory
from ppu import PPU


# setup
rom = ROM(r"tests\tetris.gb")
mem = Memory(rom)
ppu = PPU(mem)

# print buffer info
print("Starting PPU test...")

# simulate a frame  
for scanline in range(154):
    ppu.scanline = scanline

    for cycle in range(456):
        ppu.step(1)

# check some pixels in frame buffer
sample_pixels = [(0,0), (10,10), (50,50), (100,100)]
for x,y in sample_pixels:
    val = ppu.frame_buffer[y][x]
    print(f"Pixel ({x},{y}) = {val}")

print("PPU test completed")