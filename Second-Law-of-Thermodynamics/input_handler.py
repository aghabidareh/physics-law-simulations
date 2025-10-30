import pygame
from config import TEMP_MIN, TEMP_MAX


class InputHandler:
    def __init__(self, heat_system):
        self.system = heat_system
        self.heating_body1 = False
        self.cooling_body1 = False
        self.heating_body2 = False
        self.cooling_body2 = False
        
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
        if key == pygame.K_w:  # Heat body 1
            self.heating_body1 = True
        elif key == pygame.K_s:  # Cool body 1
            self.cooling_body1 = True
        
        elif key == pygame.K_UP:  # Heat body 2
            self.heating_body2 = True
        elif key == pygame.K_DOWN:  # Cool body 2
            self.cooling_body2 = True
        
        elif key == pygame.K_r:  # Reset
            self.system.reset()
        elif key == pygame.K_1:  # Preset: Hot-Cold
            self.system.body1.T = 400.0
            self.system.body2.T = 280.0
            self._update_entropies()
        elif key == pygame.K_2:  # Preset: Equal temps
            self.system.body1.T = 340.0
            self.system.body2.T = 340.0
            self._update_entropies()
        elif key == pygame.K_3:  # Preset: Cold-Hot (reverse)
            self.system.body1.T = 280.0
            self.system.body2.T = 400.0
            self._update_entropies()
    
    def _handle_keyup(self, key):
        if key == pygame.K_w:
            self.heating_body1 = False
        elif key == pygame.K_s:
            self.cooling_body1 = False
        elif key == pygame.K_UP:
            self.heating_body2 = False
        elif key == pygame.K_DOWN:
            self.cooling_body2 = False
    
    def _update_entropies(self):
        """Update entropy calculations after manual temperature change"""
        self.system.body1.S = self.system.body1._calculate_entropy()
        self.system.body2.S = self.system.body2._calculate_entropy()
        self.system.initial_total_entropy = self.system.body1.S + self.system.body2.S
        self.system.total_entropy_generated = 0.0
    
    def update(self, dt):
        """Apply continuous actions based on key states"""
        temp_change_rate = 20.0  # K/s
        
        if self.heating_body1:
            new_temp = min(self.system.body1.T + temp_change_rate * dt, TEMP_MAX)
            self.system.body1.T = new_temp
            self.system.body1.S = self.system.body1._calculate_entropy()
        elif self.cooling_body1:
            new_temp = max(self.system.body1.T - temp_change_rate * dt, TEMP_MIN)
            self.system.body1.T = new_temp
            self.system.body1.S = self.system.body1._calculate_entropy()
        
        if self.heating_body2:
            new_temp = min(self.system.body2.T + temp_change_rate * dt, TEMP_MAX)
            self.system.body2.T = new_temp
            self.system.body2.S = self.system.body2._calculate_entropy()
        elif self.cooling_body2:
            new_temp = max(self.system.body2.T - temp_change_rate * dt, TEMP_MIN)
            self.system.body2.T = new_temp
            self.system.body2.S = self.system.body2._calculate_entropy()
