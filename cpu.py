class CPU:
    def __init__(self, memory):
        self.mem = memory
        self.reg = None
        self.halted = False
        self.debug = False # enable/disable debug prints

    def connect_registers(self, registers):
        self.reg = registers

        # fetch helpers
    def fetch_byte(self):
        val = self.mem.read(self.reg.PC)
        self.reg.PC += 1
        return val
    
    def fetch_word(self):
        lo = self.fetch_byte()
        hi = self.fetch_byte()
        return (hi << 8) | lo
    
    # core step
    def execute_next(self):
        opcode = self.fetch_byte()

        # NOP
        if opcode == 0x00:
            return
             
        if self.debug:
            print(f"PC={self.reg.PC-1:#04x}, opcode={opcode:#02x}")
        
        # HALT
        if opcode == 0x76:
            self.halted = True
            return 
        
        # LD A,r 
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
            self.reg.A = val
            return
        
        # LD r,n (immediate 8-bit)
        ld_imm_map = {
            0x06: "B",
            0x0E: "C",
            0x16: "D",
            0x1E: "E",
            0x26: "H",
            0x2E: "L",
            0x3E:"A"
        }
        if opcode in ld_imm_map:
            target = ld_imm_map[opcode]
            val = self.fetch_byte()
            setattr(self.reg, target, val)
            return
        
        # LD (HL),r 
        ld_hl_r_map = {
            0x70: "B",
            0x71: "C",
            0x72: "D",
            0x73: "E",
            0x74: "H",
            0x75: "L",
            0x77: "A"
        }
        if opcode in ld_hl_r_map:
            val = getattr(self.reg, ld_hl_r_map[opcode])
            self.mem.write(self.reg.HL, val)
            return
        
        # LD (HL),n
        if opcode == 0x36:
            val = self.fetch_byte()
            self.mem.write(self.reg.HL, val)
            return
        
        # INC r
        inc_map = {0x04: "B",
                   0x0C: "C",
                   0x14: "D",
                   0x1C: "E",
                   0x24: "H",
                   0x2C: "L",
                   0x3C: "A"
                   }
        if opcode in inc_map:
            reg_name = inc_map[opcode]
            val = (getattr(self.reg, reg_name) + 1) & 0xFF
            setattr(self.reg, reg_name, val)
            return
        
        # DEC r
        dec_map = {0x05: "B",
                   0x0D: "C",
                   0x15: "D",
                   0x1D: "E",
                   0x25: "H",
                   0x2D: "L",
                   0x3D: "A"
                   }
        if opcode in dec_map:
            reg_name = dec_map[opcode]
            val = (getattr(self.reg, reg_name) -1) & 0xFF
            setattr(self.reg, reg_name, val)
            return
        
        # ADD A,r
        add_map = {0x80: "B",
                   0x81: "C",
                   0x82: "D",
                   0x83: "E",
                   0x84: "H",
                   0x85: "L",
                   0x87: "A"
                   }
        if opcode in add_map:
            val = getattr(self.reg, add_map[opcode])
            self.reg.A = (self.reg.A + val) & 0xFF
            return

        # SUB r
        sub_map = {
            0x90: "B",
            0x91: "C",
            0x92: "D",
            0x93: "E",
            0x94: "H",
            0x95: "L",
            0x97: "A"
        }
        if opcode in sub_map:
            val = getattr(self.reg, sub_map[opcode])
            self.reg.A = (self.reg.A - val) & 0xFF
            return
        
        # JP nn
        if opcode == 0xC3:
            addr = self.fetch_word()
            self.reg.PC = addr
            return
        
        # JR n
        if opcode == 0x18:
            offset = self.fetch_byte()
            if offset >= 0x80:
                offset = -((~offset + 1) & 0xFF)
            self.reg.PC += offset
            return
        
        
        # unimplemented opcode
        raise NotImplementedError(f"Opcode {opcode:#02x} not implemented") 
