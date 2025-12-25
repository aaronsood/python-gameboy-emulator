import pygame
from ppu import PPU
from memory import Memory
from cpu import CPU
from rom import ROM
from registers import Registers
# initialise pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 160, 144
WINDOW_SCALE = 3 
screen = pygame.display.set_mode((SCREEN_WIDTH * WINDOW_SCALE, SCREEN_HEIGHT * WINDOW_SCALE))
pygame.display.set_caption("GBreaker")

# colours for gameboy (yes colours i live in a bri'ish country)

GB_COLOURS = [
(224, 248, 208), # white
(136, 192, 112), # light gray
(52, 104, 86),  # dark gray
(8, 24, 32) # black
]

# setup memory cpu ppu rom and registers
rom_file = "tests/tetris.gb"
rom = ROM(rom_file)
memory = Memory(rom)

registers = Registers()
cpu = CPU(memory)
cpu.connect_registers(registers)

ppu = PPU(memory)

clock = pygame.time.Clock()
running = True

# main
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # execute one frame 
    cycles_this_frame = 0
    while cycles_this_frame < 70224:
        cycles = cpu.execute_next() or 4 
        ppu.steps(cycles)
        cycles_this_frame += cycles
        
    # render frame buffer
    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            colour_index = ppu.frame_buffer[y][x]
            colour = GB_COLOURS [colour_index]
            pygame.draw.rect(screen, colour,
                             pygame.rect(x*WINDOW_SCALE , y*WINDOW_SCALE, WINDOW_SCALE, WINDOW_SCALE))
    pygame.display.flip()
    clock.tick(60) # helps u get around 60 fps

pygame.quit()