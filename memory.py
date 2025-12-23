class Memory:
    def __init__(self, rom):
        # rom is loaded from ROM class
        self.rom = rom
        # work ram 
        self.wram = bytearray(0x2000)
        # high ram
        self.hram = bytearray(0x7F)
        self.debug = False

    def read(self, addr: int) -> int:
        # read from rom, wrom, hram
        if 0x0000 <= addr <= 0x7FFF:
            return self.rom.get_byte(addr)
        elif 0xC000 <=addr <= 0xDFFF:
            return self.wram[addr - 0xC000]
        elif 0xFF80 <=addr <= 0xFFFE:
            return self.hram[addr - 0xFF80]
        else:
            return 0xFF

    def write(self, addr: int, value: int):
        # mask value to 8 bits before writing
        value &= 0xFF
        if 0xC000 <= addr <= 0xDFFF:
            self.wram[addr - 0xC000] = value
        elif 0xFF80 <= addr <= 0xFFFE:
            self.hram[addr - 0xFF80] = value

        if self.debug:
            print(f"write{hex(value)} to {hex(addr)}")