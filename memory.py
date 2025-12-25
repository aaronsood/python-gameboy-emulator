class Memory:
    def __init__(self, rom):
        # rom is loaded from ROM class
        self.rom = rom


        # work ram 0xC000-0xDFFF
        self.wram = bytearray(0x2000)
        # high ram 0xFF80-0xFFFE
        self.hram = bytearray(0x7F)
        # video ram 0x8000-0x9FFF
        self.vram = bytearray(0x2000)
        # io registers 0xFF00-0xFF7F
        self.io = bytearray(0x80)

        self.debug = False

    def read(self, addr: int) -> int:
        # ROM
        if 0x0000 <= addr <= 0x7FFF:
            return self.rom.get_byte(addr)
        # VRAM
        elif 0x8000 <= addr <= 0x9FFF:
            return self.vram[addr - 0x8000]
        # WRAM
        elif 0xC000 <=addr <= 0xDFFF:
            return self.wram[addr - 0xC000]
        # IO registers
        elif 0xFF00 <= addr <= 0xFF7F:
            return self.io[addr - 0xFF00]
        # HRAM
        elif 0xFF80 <=addr <= 0xFFFE:
            return self.hram[addr - 0xFF80]
        else:
            return 0xFF
    

    def write(self, addr: int, val: int):
        # mask value to 8 bits before writing
        val &= 0xFF

        # VRAM
        if 0x8000 <= addr <= 0x9FFF:
            self.vram[addr - 0x8000] = val
        # WRAM
        elif 0xC000 <= addr <= 0xDFFF:
            self.wram[addr - 0xC000] = val
        # IO registers
        elif 0xFF00 <= addr <= 0xFF7F:
            self.io[addr - 0xFF00] = val
        # HRAM
        elif 0xFF80 <= addr <= 0xFFFE:
            self.hram[addr - 0xFF80] = val

        if self.debug:
            print(f"write {hex(val)} to {hex(addr)}")