import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  
from registers import Registers
r = Registers()
r.BC = 0x1234
print(f"BC: {hex(r.BC)}, B: {hex(r.B)}, C: {hex(r.C)}")
assert r.B == 0x12
assert r.C == 0x34
assert r.BC == 0x1234
r.A = 0x56
r.F = 0xF0
assert r.A == 0x56
assert r.F == 0xF0
assert r.AF == 0x56F0
r.HL = 0xABCD
assert r.H == 0xAB
assert r.L == 0xCD
print("All register tests passed.")