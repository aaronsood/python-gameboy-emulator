import sys
import os
import pygame   

# add parent folder to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rom import ROM
from memory import Memory
from ppu import PPU

# print buffer info
print("Script started", flush = True)

# setup
rom = ROM(r"tests\tetris.gb")
mem = Memory(rom)
ppu = PPU(mem)

mem.write(0xFF40, 0x01)
mem.write(0xFF42, 0x00)
mem.write(0xFF43, 0x00)
mem.write(0xFF47, 0xE4)

for tile in range(0, 32):
    base = 0x8000 + tile * 16   
    for row in range(8):
        if row % 2 == 0:
            mem.write(base + row*2,    0b10101010)
            mem.write(base + row*2 + 1, 0b01010101)
        else:
            mem.write(base + row*2,    0b01010101)
            mem.write(base + row*2 + 1, 0b10101010)

for i in range (32*32):
    mem.write(0x9800 + i, i % 32)

for _ in range(70224):
    ppu.step(1)

print("Frame rendered,", flush=True)
        


# display the frame with pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 160, 144
WINDOW_SCALE = 3
screen = pygame.display.set_mode((SCREEN_WIDTH*WINDOW_SCALE, SCREEN_HEIGHT*WINDOW_SCALE))
pygame.display.set_caption("GBreaker")

GB_COLOURS = [
    (224, 248, 208),
    (136, 192, 112),
    (52, 104, 86),
    (8, 24, 32) 
]

for y in range(SCREEN_HEIGHT):
    for x in range(SCREEN_WIDTH):
        colour_index = ppu.frame_buffer[y][x]
        colour = GB_COLOURS[colour_index]
        pygame.draw.rect(screen, colour, pygame.Rect(x*WINDOW_SCALE, y*WINDOW_SCALE, WINDOW_SCALE, WINDOW_SCALE))

pygame.display.flip()   

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        clock.tick(60)
pygame.quit()
print("PPU test completed", flush = True)

