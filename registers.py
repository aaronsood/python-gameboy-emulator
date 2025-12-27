class Registers:
        def __init__(self):
         self.A = 0
         self.F = 0
         self.B = 0
         self.C = 0
         self.D = 0
         self.E = 0
         self.H = 0
         self.L = 0
         self.SP = 0
         self.PC = 0

        # 16-bit combined registers
        @property
        def AF(self):
            return self._AF
        
        @AF.setter
        def AF(self, val):
            if self.debug: print("Setting AF", hex(val))
            self._AF = val & 0xFFFF   

        #BC register
        @property
        def BC(self):
            return self._BC
        
        @BC.setter
        def BC(self, val):
            tmp = val  & 0xFFFF
            self._BC = tmp
            if self.debug: print("BC set to", hex(self._BC))

        #DE register
        @property
        def DE(self):
            return self._DE
        
        @DE.setter
        def DE(self, val):
            self._DE = val & 0xFFFF

        # HL register
        @property
        def HL(self):
            return self._HL
        
        @HL.setter
        def HL (self, val):
            self._HL = val & 0xFFFF    

        # flag helpers (z n h c)
        @property
        def Z(self):
            return (self.F >> 7) & 1
        
        @Z.setter
        def Z(self, v):
            self.F = (self.F & ~(1 << 7)) | ((v & 1) << 7)

        @property
        def N(self):
            return (self.F >> 6) & 1
        
        @N.setter 
        def N(self, v):
            self.F = (self.F & ~(1 << 6)) | ((v & 1) << 6)
        
        @property
        def H(self):
            return (self.F >> 5) & 1
        
        @H.setter
        def H(self,v):
            self.F = (self.F & ~(1 << 5)) | ((v & 1) << 5)  

        @property
        def Cflag(self):
            return (self.F >> 4) & 1
        
        @Cflag.setter
        def Cflag (self, v):
            self.F = (self.F & ~(1 << 4)) | ((v & 1) << 4)
