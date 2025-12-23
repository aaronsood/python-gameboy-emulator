#coded by aaronsood
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from rom import ROM
rom = ROM("tests/cpu_instrs.gb")
print("ROM title:", rom.title)
print("Cartridge type:", rom.cartridge_type)
print("ROM size byte:", rom.rom_size)
print("First 16 bytes of ROM:")
print([hex(b) for b in rom.data[:16]])
