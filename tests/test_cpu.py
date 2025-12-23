import sys 
import os

# add parent folder to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rom import ROM
from memory import Memory
from registers import Registers
from cpu import CPU

# setup rom, memory, registers, cpu
rom = ROM(r"tests\cpu_instrs.gb")
mem = Memory(rom)
reg = Registers()
cpu = CPU(mem)
cpu.connect_registers(reg)

# store starting pc
start_pc = reg.PC

# fetch first byte
byte = cpu.fetch_byte()
print(f"fetched byte: {hex(byte)}")

# pc should have incremented by 1
assert reg.PC == start_pc + 1

# test execute next (currently just handles nop)
cpu.execute_next() # this will either do nothing or print unimplemented opcode

print("CPU basic test + nop test passed.")