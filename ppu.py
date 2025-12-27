import pygame

# initialise pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 160, 144
WINDOW_SCALE = 3 

GB_COLOURS = [
(224, 248, 208), # white
(136, 192, 112), # light gray
(52, 104, 86),  # dark gray
(8, 24, 32) # black
]

class PPU:
    def __init__(self, memory):
        self.mem = memory

        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        self.frame_buffer = [[0]*self.SCREEN_WIDTH for _ in range(self.SCREEN_HEIGHT)]

        self.scanline = 0
        self.cycle = 0
        self.mode = 2

        def request_interrupt(self, bit):
            val = self.mem.read(0xFF0F)
            self.mem.write(0xFF0F, val | (1 << bit))
    
    def get_tile_address(self, tile_index, signed_mode):
        if signed_mode: 
            tile_index = (tile_index + 128) % 256 - 128
            base = 0x9000
        else:
            base = 0x8000
        return (base + tile_index * 16) & 0xFFFF
    
    # decode 2-bit pixel
    def decode_tile_pixel(self, lo, hi, bit):
        lo_b = (lo >> bit) & 1
        hi_b = (hi >> bit) & 1
        return (hi_b << 1) | lo_b
    
    # map pixel using BGP
    def map_colour_bgp(self, palette, value):
        shift = value * 2
        return (palette >> shift) & 3
    
    def step(self, cycles):
        lcdc = self.mem.read(0xFF40)

        if not (lcdc & 0x80):
            self.mode = 0
            self.scanline = 0
            self.cycle = 0
            self.mem.write(0xFF44, 0)
            return
        
        if self.scanline < 144:
            if self.cycle < 80:
                self.mode = 2
            elif self.cycle < 252: 
                self.mode = 3
            else:
                if self.mode == 3:
                    self.render_scanline(self.scanline, lcdc)
                self.mode = 0   
        else:
            self.mode = 1

        stat = self.mem.read(0xFF41) & ~0b11
        self.mem.write(0xFF41, stat | self.mode)

        if self.cycle >= 456:
            self.cycle -= 456
            self.scanline += 1
            self.mem.write(0xFF44, self.scanline)
            
            if self.scanline == 144:
                self.request_interrupt(0)
            
            if self.scanline >= 154:
                self.request_interrupt(0)
                self.mem.write(0xFF44, 0)


    def render_scanline(self, line, lcdc):
        bg_map = 0x9C00 if (lcdc & 0x08) else 0x9800
        bg_signed = not (lcdc & 0x10)

        scx = self.mem.read(0xFF43)
        scy = self.mem.read(0xFF42)

        wy = self.mem.read(0xFF4A)
        wx = self.mem.read(0xFF4B) - 7
        
        window_enabled = (lcdc & 0x20) and (line >= wy)
        bgp = self.mem.read(0xFF47)

        for x in range(self.SCREEN_WIDTH):

            use_window = window_enabled and x >= wx

        if use_window:
            win_map = 0x9C00 if (lcdc & 0x40)  else 0x9800
            wx_x = x - wx   
            wy_y = line - wy 

            tile_row = (wy_y // 8) * 32
            tile_col = wx_x // 8

            tile_index = self.mem.read(win_map + tile_row + tile_col)
            tile_addr = self.get_tile_address(tile_index, bg_signed)

            row = (wy % 8) * 2
        
        else:
            y = (line + scy) & 0xFF
            tile_row = (y // 8) * 32

            x_bg = (x + scx) & 0xFF 
            tile_col = x_bg // 8

            tile_index = self.mem.read(win_map + tile_row + tile_col)
            tile_addr = self.get_tile_address(tile_index, bg_signed)

            row = (y % 8) * 2

        lo = self.mem.read(tile_addr + row)
        hi = self.mem.read(tile_addr + row + 1)
        
        bit = 7 - (x % 8)
        value = self.decode_tile_pixel(lo, hi, bit)

        colour = self.map_colour (bgp, value)
        self.frame_buffer[line][x] = colour

    def render_sprites(self, line, lcdc):
        if not(lcdc & 0x02): 
            return
        
        sprite_height = 16 if (lcdc & 0x04) else 8

        for i in range(40):
            oam = 0xFE00 + i * 4
            
            y = self.mem.read(oam) - 16
            x = self.mem.read(oam + 1) - 8
            tile = self.mem.read(oam + 2)
            flags = self.mem.read(oam + 3)

            if not (y <= line < y + sprite_height):
                continue    

            flip_y = flags & 0x40
            flip_x = flags & 0x20
            use_obj1 = flags & 0x10

            palette_addr = 0xFF49 if use_obj1 else 0xFF48
            palette = self.mem.read(palette_addr)

            row = line - y
            if flip_y:
                row = sprite_height - 1 - row
            
            tile_addr = 0x8000 + tile * 16 + row * 2
            lo = self.mem.read(tile_addr)
            hi = self.mem.read(tile_addr + 1)

            for px in range(8):
                sx = x + (7 - px if flip_x else px)
                if sx < 0 or sx >= 160:
                    continue

                bit = 7 - px    
                val = self.decode_tile_pixel(lo, hi, bit)
                if val == 0:    
                    continue
                
                colour = self.map_colour(palette, val)
                self.frame_buffer[line][sx] = colour




def draw_frame(ppu, screen):
    for y in range(ppu.SCREEN_HEIGHT):
        for x in range(ppu.SCREEN_WIDTH):
            colour = GB_COLOURS[ppu.frame_buffer[y][x]]
            pygame.draw.rect (screen, colour, pygame.Rect(x*WINDOW_SCALE, y*WINDOW_SCALE,  WINDOW_SCALE, WINDOW_SCALE))
    pygame.display.flip()