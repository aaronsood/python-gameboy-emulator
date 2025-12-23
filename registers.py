class Registers:
        def __init__(self):
            # 16-bit regs, some default gameboy startup values
            self._AF = 0x01B0 # A = 0x01, F = 0xB0
            self._BC = 0x1234
            self._DE = 0x00D8
            self._HL = 0x014D
            self.SP = 0xFFFE
            self.PC = 0x0100

        # optional debug hook
            self.debug = False

        #AF registers and flags

        @property
        def AF(self):
            return self._AF
        
        @AF.setter
        def AF(self, val):
            if self.debug: print("Setting AF", hex(val))
            self._AF = val & 0xFFFF   

        @property
        def A(self):
            return (self._AF >> 8) & 0xFF
        
        @A.setter
        def A(self, val): 
            self._AF = ((val & 0xFF) << 8) | (self._AF & 0xFF)

        @property
        def F(self):
            # only upper 4 bits are flags, lower 4 ignored
            return self._AF & 0xF0
        
        @F.setter
        def F(self, val):
            self._AF = (self._AF & 0xFF00) | (val & 0xF0)

        #BC register

        @property
        def BC(self):
            return self._BC
        
        @BC.setter
        def BC(self, val):
            tmp = val  & 0xFFFF
            self._BC = tmp
            if self.debug: print("BC set to", hex(self._BC))

        @property
        def B(self):
            b_val = (self._BC >> 8) & 0xFF
            return b_val
        
        @B.setter
        def B(self, val):
            c_reg = self.BC & 0xFF
            self._BC = ((val & 0xFF) << 8) | (self._BC & 0xFF)

        @property
        def C(self):
            return self._BC & 0xFF
        
        @C.setter
        def C(self, val):   
            b_val = self._BC >> 8
            self._BC = (b_val << 8) | (val & 0xFF)

        #DE register

        @property
        def DE(self):
            return self._DE
        
        @DE.setter
        def DE(self, val):
            self._DE = val & 0xFFFF

        @property
        def D(self):
            return (self._DE >> 8) & 0xFF
        
        @D.setter
        def D(self, val):
            self._DE = ((val & 0xFF) << 8) | (self._DE & 0xFF)

        @property
        def E(self):
            return self._DE & 0xFF
        
        @E.setter
        def E(self, val):
            d_high = self._DE >> 8
            self._DE = (d_high << 8) | (val & 0xFF)

        # HL register

        @property
        def HL(self):
            return self._HL
        
        @HL.setter
        def HL (self, val):
            self._HL = val & 0xFFFF    

        @property
        def H(self):
            return (self._HL >> 8) & 0xFF
        
        @H.setter
        def H(self, val):
            l_val = self.HL & 0xFF
            self._HL = ((val & 0xFF) << 8) | l_val

        @property
        def L(self):
            return self._HL & 0xFF
        
        @L.setter
        def L(self, val):
            h_val = self._HL >> 8
            self._HL = (h_val << 8) | (val & 0xFF)