class CPU:
    def __init__(self, memory):
        # store memory instance
        self.mem = memory
        # registers will also be connected later
        self.reg = None
        self.halted = False # cpu is running by default

    def connect_registers(self, registers):
        # attach registers to cpu
        self.reg = registers
    
    def fetch_byte(self):
        # read byte from memory at pc and increment pc
        pc = self.reg.PC
        val = self.mem.read(pc)
        self.reg.PC += 1
        return val
    
    # placeholder for instruction execution
    def execute_next(self):
    # fetch opcode
        opcode = self.fetch_byte()
        # for now, just handle nop (0x00)
        if opcode == 0x00:
            pass # do nothing
        
        # handle LD r,r (just a few examples for now)
        elif opcode == 0x78: # LD A,B
            self.reg.A = self.reg.B
        elif opcode == 0x79: # LD A,C
            self.reg.A = self.reg.C
        elif opcode == 0x7A: # LD A,D
            self.reg.A = self.reg.D
        elif opcode == 0x7B: # LD A,E
            self.reg.A = self.reg.E
        elif opcode == 0x7C: # LD A,H
            self.reg.A = self.reg.H
        elif opcode == 0x7D: # LD A,L
            self.reg.A = self.reg.L
        elif opcode == 0x7F: # LD A,A
            self.reg.A = self.reg.A
        
        else:
            # placeholder for unimplemented opcodes
            print(f"Opcode {hex(opcode)} not implemented yet")