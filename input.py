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
    pygame.event.pump
    keys = pygame.key.get_pressed()

    for key, name in KEY_MAP.items():
        BUTTONS[name] = 0 if keys[key] else 1

    joyp = memory.read(0xFF00)

    select_dpad = not (joyp & 0x10)
    select_buttons = not (joyp & 0x20)
    

    val = 0xFF

    if select_dpad:
        val &= ~(BUTTONS['RIGHT'] << 0)
        val &= ~(BUTTONS['LEFT'] << 1)
        val &= ~(BUTTONS['UP'] << 2)
        val &= ~(BUTTONS['DOWN'] << 3)

    if select_buttons:
        val &= ~(BUTTONS['A'] << 0)
        val &= ~(BUTTONS['B'] << 1)
        val &= ~(BUTTONS['SELECT'] << 2)
        val &= ~(BUTTONS['START'] << 3)
    
    memory.write(0xFF00, val)