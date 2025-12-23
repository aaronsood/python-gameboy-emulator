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
        else:
            # simple placeholder for unimplemented opcodes
            print(f"opcode {hex(opcode)} not implemented yet")