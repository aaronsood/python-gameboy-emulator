import pygame, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from memory import Memory
from rom import ROM
from input import poll_input

pygame.init()
screen = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Input test")

rom = ROM("tests/tetris.gb")
mem = Memory(rom)   

mem.write(0xFF00, 0x00)

print("Press keys (Z/X/Arrows/Enter/Right Shift). Close window to exit. \n")

running = True
clock = pygame.time.Clock()
last_val = None

while running:
    pygame.event.pump()

    orig_joyp = mem.read(0xFF00)
    
    mem.write(0xFF00, 0x10)
    poll_input(mem)
    joyp_dpad = mem.read(0xFF00)

    mem.write(0xFF00, 0x20)
    poll_input(mem)
    joyp_buttons = mem.read(0xFF00)

    combined = (joyp_dpad & 0x0F) & (joyp_buttons & 0x0F)

    joyp = (orig_joyp & 0xF0) | combined
    mem.write(0xFF00, joyp)

    if joyp != last_val:
        print(f"JOYP = {joyp:08b} (0x{joyp:02x})")
        last_val = joyp 

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

            
    clock.tick(60)
    
pygame.quit()
