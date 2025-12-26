import sys
import os

# add parent folder to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rom import ROM
from memory import Memory
from ppu import PPU

# print buffer info
print("Script started", flush = True)

# setup
rom = ROM(r"tests\tetris.gb")
mem = Memory(rom)
ppu = PPU(mem)

# sanity check 
try:
    ppu.step(1)
    print("First step ok", flush = True)
except Exception as e:
    print("Error during first step:", e)
    raise

# simulate a frame  
try:
    for scanline in range(154):
        ppu.scanline = scanline
    for cycle in range(456):
        ppu.step(1)

        print("Frame simulation complete", flush=True)

except Exception as e:
    print("Error during frame:", e)
    raise
    
# check some pixels in frame buffer
print("Sampling pixels...", flush=True)

sample_pixels = [(0,0), (10,10), (50,50), (100,100)]
for x,y in sample_pixels:
    try:
        val = ppu.frame_buffer[y][x]
        print(f"Pixel ({x},{y}) = {val}")
    except Exception as e:
        print(f"Error reading pixel ({x}, {y}):", e)

print("PPU test completed", flush = True)