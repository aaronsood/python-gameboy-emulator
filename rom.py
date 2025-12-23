class ROM:
    def __init__(self, path):
        with open (path, "rb") as f:
         self.data = f.read()

        self.title = self.data[0x134:0x144].decode("ascii").strip()
        self.cartridge_type = self.data[0x147]
        self.rom_size = self.data[0x148]
    def get_byte(self, address):
       return self.data[address]