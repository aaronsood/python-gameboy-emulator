
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from rom import ROM
# simple test to check rom loading and header values
rom = ROM("tests/tetris.gb")

print("ROM title:", rom.title)
print("Cartridge type:", rom.cartridge_type)
print("ROM size byte:", rom.rom_size)
# first 16 bytes of the rom
print("First 16 bytes of ROM:")
# check one random byte for curiosity
print([hex(b) for b in rom.data[:16]])