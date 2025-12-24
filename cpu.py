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
    
    def execute_next(self):
        # fetch opcode
        opcode = self.fetch_byte()

        # handle NOP
        if opcode == 0x00:
            return
        
        # handle LD A,r 
        ld_map = {
            0x78: "B",
            0x79: "C",
            0x7A: "D",
            0x7B: "E",
            0x7C: "H",
            0x7D: "L",
            0x7F: "A",
        }

        if opcode in ld_map:
            src = ld_map[opcode]
            val = getattr(self.reg, src)
            # optional debug print
            print(f"Before execute: PC={self.reg.PC-1:#04x}, {src}={val:#02x}, A={self.reg.A:#02X}")
            self.reg.A = val
            print(f"After execute: PC={self.reg.PC:#04x}, {src}={getattr(self.reg, src):#02x}, A={self.reg.A:#02X}")
            return
        
        # placeholder for unimplemented opcodes 
        print(f"Opcode {hex(opcode)} not implemented yet")