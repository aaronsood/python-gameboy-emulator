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

# helper to test LD r,r
def test_ld_rr(target_reg, source_reg, opcode, val):
    reg.PC = 0xC000 # reset PC
    setattr(reg, source_reg, val) # set source register
    mem.write(reg.PC, opcode) # write opcode to memory
    print(f"Before execute: PC={reg.PC:#04x}, {source_reg}={getattr(reg, source_reg):#02x}, {target_reg}={getattr(reg, target_reg):#02x}")
    cpu.execute_next()
    print(f"After execute: PC={reg.PC:#04x}, {source_reg}={getattr(reg, source_reg):#02x}, {target_reg}={getattr(reg, target_reg):#02x}")
    assert getattr(reg, target_reg) == val, f"{target_reg} != {val:#02x}"
    print(f"LD {target_reg},{source_reg} passed: {val:#02x}")

# LD A,r tests
test_ld_rr("A", "B", 0x78, 0x12)
test_ld_rr("A", "C", 0x79, 0x34)
test_ld_rr("A", "D", 0x7A, 0x56)
test_ld_rr("A", "E", 0x7B, 0x78)
test_ld_rr("A", "H", 0x7C, 0x9A)
test_ld_rr("A", "L", 0x7D, 0xBC)
test_ld_rr("A", "A", 0x7F, 0xDE)

print("Basic LD r,r tests passed")

# PC increment test
start_pc = 0xC200
reg.PC = start_pc
mem.write(reg.PC, 0x00) # NOP
byte = cpu.fetch_byte()
assert byte == 0x00
assert reg.PC == start_pc + 1
print("fetch_byte() test passed")

# NOP test
reg.PC = 0xC300
mem.write(reg.PC, 0x00)
cpu.execute_next() # should do nothing
print("NOP test passed")