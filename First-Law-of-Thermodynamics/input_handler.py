import pygame
from config import HEAT_RATE


class InputHandler:
    def __init__(self, gas_system):
        self.gas = gas_system
        self.heating = False
        self.cooling = False
        self.compressing = False
        self.expanding = False
        
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)
            
            elif event.type == pygame.KEYUP:
                self._handle_keyup(event.key)
        
        return True
    
    def _handle_keydown(self, key):
        if key == pygame.K_h:
            self.heating = True
        elif key == pygame.K_c:
            self.cooling = True
        elif key == pygame.K_UP:
            self.compressing = True
        elif key == pygame.K_DOWN:
            self.expanding = True
        elif key == pygame.K_r:
            self.gas.reset()
    
    def _handle_keyup(self, key):
        if key == pygame.K_h:
            self.heating = False
        elif key == pygame.K_c:
            self.cooling = False
        elif key == pygame.K_UP:
            self.compressing = False
        elif key == pygame.K_DOWN:
            self.expanding = False
    
    def update(self, dt):
        if self.heating:
            self.gas.add_heat(HEAT_RATE, dt)
        elif self.cooling:
            self.gas.add_heat(-HEAT_RATE, dt)

        compression_force = 0.0
        if self.compressing:
            compression_force = -50.0
        elif self.expanding:
            compression_force = 50.0
        
        if compression_force != 0.0:
            self.gas.compress_expand(compression_force, dt)
