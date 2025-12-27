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
        
        # INC (HL)
        if opcode == 0x34:
            val = (self.mem.read(self.reg.HL) + 1) & 0xFF
            self.mem.write(self.reg.HL, val)
            return
        
        # DEC (HL)
        if opcode == 0x35:
            val = (self.mem.read(self.reg.HL) - 1) & 0xFF
            self.mem.write(self.reg.HL, val)
            return
        
        # LD A,(HL)
        if opcode == 0x7E: 
            self.reg.A = self.mem.read(self.reg.HL)
            return
        
        # LD (HL), A
        if opcode == 0x77:
            self.mem.write(self.reg.HL, self.reg.A)
            return

        # LD rr,nn (16-bit immediate loads)
        ld_rr_imm = {
            0x01: "BC",
            0x11: "DE",
            0x21: "HL",
            0x31: "SP",
        }
        if opcode in ld_rr_imm:
            val = self.fetch_word()
            setattr(self.reg, ld_rr_imm[opcode], val)
            return
        
        # LD (HL+),A
        if opcode == 0x22:
                self.mem.write(self.reg.HL, self.reg.A)
                self.reg.HL = (self.reg.HL + 1) & 0xFFFF
                return
        # LD (HL-), A
        if opcode == 0x32:
            self.mem.write(self.reg.HL, self.reg.A)
            self.reg.HL = (self.reg.HL - 1) & 0xFFFF
        
        # LD A,(BC)
        if opcode == 0x0A:
            self.reg.A = self.mem.read(self.reg.BC)
            return
        
        # LD A,(DE)
        if opcode == 0x1A:
            self.reg.A = self.mem.read(self.reg.DE)
        
        # LD A,(nn)
        if opcode == 0xFA:
            addr = self.fetch_word()
            self.reg.A = self.mem.read(addr)
            return
        
        # LD (nn),A
        if opcode == 0xEA:
            addr = self.fetch_word()
            self.mem.write(addr, self.reg.A)
            return
        
        # INC rr
        inc_rr = {
            0x03: "BC",
            0x13: "DE",
            0x23: "HL",
            0x33: "SP"
        }
        if opcode in inc_rr:
            name = inc_rr[opcode]
            setattr(self.reg, name, (getattr(self.reg, name) + 1) & 0xFFFF)
            return
        
        # DEC rr
        dec_rr = {
            0x0B: "BC",
            0x1B: "DE",
            0x2B: "HL",
            0x3B: "SP"
        }
        if opcode in dec_rr:
            name = dec_rr[opcode]
            setattr(self.reg, name, (getattr(self.reg, name) -1) & 0xFFFF)
            return  
        
        # ADD HL,rr
        add_hl = {
            0x09: "BC",
            0x19: "DE",
            0x29: "HL",
            0x39: "SP"
        }
        if opcode in add_hl:
            val = getattr(self.reg, add_hl[opcode])
            self.reg.HL = (self.reg.HL + val) & 0xFFFF
            return
        
        # XOR A
        if opcode == 0xAF:
            self.reg.A = 0
            return
        
        # AND n
        if opcode == 0xE6:
            self.reg.A &= self.fetch_byte()
            return
        
        # OR n
        if opcode == 0xF6:
            self.reg.A |= self.fetch_byte()
            return
        
        # JR Z,n
        if opcode == 0x28:
            off = self.fetch_byte()
            if self.reg.Z: # if zero flag set
                if off >= 0x80: off -= 0x100
                self.reg.PC = (self.reg.PC+ off) & 0xFFFF
                return
            
        # JR NZ,n
        if opcode == 0x20:
            off = self.fetch_byte()
            if not self.reg.Z:
                if off >= 0x80: off -= 0x100
                self.reg.PC = (self.reg.PC + off) & 0xFFFF
                return
            
        # PUSH rr
        push_rr = {
            0xC5: "BC",
            0xD5: "DE",
            0xE5: "HL",
            0xF5: "AF"
        }
        if opcode in push_rr:
            val = getattr(self.reg, push_rr[opcode])
            self.reg.SP = (self.reg.SP - 2) & 0xFFFF
            self.mem.write_word(self.reg.SP, val)
            return
        
        # POP rr
        pop_rr = { 
            0xC1: "BC",
            0xD1: "DE",
            0xE1: "HL",
            0xF1: "AF"
        }
        if opcode in pop_rr:
            val = self.mem.read_word(self.reg.SP)
            self.reg.SP = (self.reg.SP + 2) & 0xFFFF
            setattr(self.reg, pop_rr[opcode], val)
            return
        
        # CALL nn
        if opcode == 0xCD:
            addr = self.fetch_word()
            self.reg.SP = (self.reg.SP -2) & 0xFFFF
            self.mem.write_word(self.reg.SP, self.reg.PC)
            self.reg.PC = addr
            return
        
        # RET
        if opcode == 0xC9:
            self.reg.PC = self.mem.read_word(self.reg.SP)
            self.reg.SP = (self.reg.SP + 2) & 0xFFFF
            return
        
            # unimplemented opcode
            raise NotImplementedError(f"Opcode {opcode:#02x} not implemented") 
