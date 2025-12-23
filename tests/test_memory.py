import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from rom import ROM
from memory import Memory
rom = ROM("tests/cpu_instrs.gb")
mem = Memory(rom)
print("ROM byte @ 0x100:", hex(mem.read(0x100)))
mem.write(0xC000, 0x42)
print("WRAM byte @ 0xC000:", hex(mem.read(0xC000)))
mem.write(0xFF80, 0x99)
print("HRAM byte @ 0xFF80:", hex(mem.read(0xFF80))) 