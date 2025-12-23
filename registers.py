class Registers:
    def __init__(self):
        self._AF = 0x01B0
        self._BC = 0x1234
        self._DE = 0x00D8
        self._HL = 0x014D
        self.SP = 0xFFFE
        self.PC = 0x0100
    @property
    def AF(self):
        return self._AF
    @AF.setter
    def AF(self, value):
        self._AF = value & 0xFFFF
    @property
    def A(self):
        return (self._AF >> 8) & 0xFF
    @A.setter
    def A(self, value): 
        self._AF = ((value & 0xFF) << 8) | (self._AF & 0xFF)
    @property
    def F(self):
        return self._AF & 0xF0
    @F.setter
    def F(self, value):
        self._AF = (self._AF & 0xFF00) | (value & 0xF0)
    @property
    def BC(self):
        return self._BC
    @BC.setter
    def BC(self, value):
        self._BC = ((value & 0xFF) << 8) | (self._BC & 0xFF)
    @property
    def B(self):
        return(self._BC >> 8) & 0xFF
    @B.setter
    def B(self, value):
        self._BC = ((value & 0xFF) << 8) | (self._BC & 0xFF)
    @property
    def C(self):
        return self._BC & 0xFF
    @C.setter
    def C(self, value):
        self._BC = (self._BC & 0xFF00) | (value & 0xFF)
    @property
    def DE(self):
        return self._DE
    @DE.setter
    def DE(self, value):
        self._DE = value & 0xFFFF
    @property
    def D(self):
        return (self._DE >>8) & 0xFF
    @D.setter
    def D(self, value):
        self._DE = ((value & 0xFF) << 8) | (self._DE & 0xFF)
    @property
    def E(self):
        return self._DE & 0xFF
    @E.setter
    def E(self, value):
        self._DE = (self._DE & 0xFF00) | (value & 0xFF)
    @property
    def HL(self):
        return self._HL
    @HL.setter
    def HL (self, value):
        self._HL = value & 0xFFFF    
    @property
    def H(self):
        return (self._HL >> 8) & 0xFF
    @H.setter
    def H(self, value):
        self._HL = ((value & 0xFF) << 8) | (self._HL & 0xFF)
    @property
    def L(self):
        return self._HL & 0xFF
    @L.setter
    def L(self, value):
        self._HL = (self._HL & 0xFF00) | (value & 0xFF)