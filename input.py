import pygame

KEY_MAP = {
    pygame.K_RIGHT: 'RIGHT',
    pygame.K_LEFT: 'LEFT',
    pygame.K_UP: 'UP',
    pygame.K_DOWN: 'DOWN',
    pygame.K_z: 'A',
    pygame.K_x: 'B',
    pygame.K_RETURN: 'START',
    pygame.K_RSHIFT: 'SELECT'
}
BUTTONS = {
    'RIGHT': 1,
    'LEFT': 1,
    'UP': 1,
    'DOWN': 1,
    'A': 1,
    'B': 1,
    'START': 1,
    'SELECT': 1
}

def poll_input(memory):
    # 0 means pressed 1 = released
    keys = pygame.key.get_pressed()

    for key, name in KEY_MAP.items():
        BUTTONS[name] = 0 if keys[key] else 1

    reg = memory.read(0xFF00)

    p14 = not (reg & 0x10)
    p15 = not (reg & 0x20)
    
    val = 0xFF

    if p14:
        val &= ~(BUTTONS['RIGHT'] << 0)
        val &= ~(BUTTONS['LEFT'] << 1)
        val &= ~(BUTTONS['UP'] << 2)
        val &= ~(BUTTONS['DOWN'] << 3)

    if p15:
        val &= ~(BUTTONS['A'] << 0)
        val &= ~(BUTTONS['B'] << 1)
        val &= ~(BUTTONS['SELECT'] << 2)
        val &= ~(BUTTONS['START'] << 3)
    
    memory.write(0xFF00, val)g