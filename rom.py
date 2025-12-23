class ROM:
    def __init__(self, path):
        # read entire rom into memory
        with open (path, "rb") as f:
         self.data = f.read()

        # header values from gb rom spec
        self.title = self.data[0x134:0x144].decode("ascii", errors="ignore").strip()
        self.cartridge_type = self.data[0x147]
        self.rom_size = self.data[0x148]

    def get_byte(self, address):
       if address < 0 or address >= len(self.data):
          return 0xFF
       return self.data[address]