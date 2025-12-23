class Memory:
    def __init__(self, rom):
        self.rom = rom
        self.wram = bytearray(0x2000)
        self.hram = bytearray(0x7F)
    def read(self, addr: int) -> int:
        if 0x0000 <= addr <= 0x7FFF:
            return self.rom.get_byte(addr)
        elif 0xC000 <=addr <= 0xDFFF:
            return self.wram[addr - 0xC000]
        elif 0xFF80 <=addr <= 0xFFFE:
            return self.hram[addr - 0xFF80]
        else:
            return 0xFF
    def write(self, addr: int, value: int):
        value &= 0xFF
        if 0xC000 <= addr <= 0xDFF:
            self.wram[addr - 0xC000] = value
        elif 0xFF80 <= addr <= 0xFFFE:
            self.hram[addr - 0xFF80] = value