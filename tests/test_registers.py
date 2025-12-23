import sys
import os

# add parent folder to path to import registers
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from registers import Registers

# make a registers instance
r = Registers()
r.debug = True # optional debug prints

# test BC register
r.BC = 0x1234  
print(f"BC: {hex(r.BC)}, B: {hex(r.B)}, C: {hex(r.C)}")
assert r.B == 0x12
assert r.C == 0x34
assert r.BC == 0x1234

# test AF register
r.A = 0x56
r.F = 0xF0
assert r.A == 0x56
assert r.F == 0xF0
assert r.AF == 0x56F0

# test HL register
r.HL = 0xABCD
assert r.H == 0xAB
assert r.L == 0xCD

# optional casual debug   
if r.debug:
    print("Registers tests done.")
    
print ("All registers passed.")