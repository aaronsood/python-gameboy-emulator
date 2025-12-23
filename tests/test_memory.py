import sys
import os

# add parent directory to path so we can import rom and memory
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from rom import ROM
from memory import Memory

# load test rom and memory
rom = ROM("tests/cpu_instrs.gb")
mem = Memory(rom)
# test rom read
print("ROM byte @ 0x100:", hex(mem.read(0x100)))

# test writing to work RAM
mem.write(0xC000, 0x42)
print("WRAM byte @ 0xC000:", hex(mem.read(0xC000)))

# test writing to high RAM
mem.write(0xFF80, 0x99)
print("HRAM byte @ 0xFF80:", hex(mem.read(0xFF80))) 