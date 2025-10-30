import pygame
import numpy as np


class InputHandler:
    def __init__(self, pendulum):
        self.pendulum = pendulum
        self.dragging = False
        self.mouse_pos = None
        
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                bob_pos = self.pendulum.get_position()
                distance = np.linalg.norm(np.array(pos) - bob_pos)
                
                if distance <= self.pendulum.radius + 10:
                    self.dragging = True
                    self.mouse_pos = pos
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragging:
                    if self.mouse_pos:
                        mouse_current = pygame.mouse.get_pos()
                        dx = mouse_current[0] - self.mouse_pos[0]
                        dy = mouse_current[1] - self.mouse_pos[1]
                        impulse = np.sqrt(dx**2 + dy**2) * 0.1
                        if dx > 0:
                            self.pendulum.apply_impulse(impulse)
                        else:
                            self.pendulum.apply_impulse(-impulse)
                    
                self.dragging = False
                self.mouse_pos = None
            
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                pos = pygame.mouse.get_pos()
                self.mouse_pos = pos
                dx = pos[0] - self.pendulum.pivot[0]
                dy = pos[1] - self.pendulum.pivot[1]
                angle = np.arctan2(dx, dy)
                self.pendulum.set_angle(angle)
            
            elif event.type == pygame.KEYDOWN:
                self._handle_key(event.key)
        
        return True
    
    def _handle_key(self, key):
        if key == pygame.K_r:
            self.pendulum.reset()
        elif key == pygame.K_UP:
            self.pendulum.set_length(self.pendulum.length + 10)
        elif key == pygame.K_DOWN:
            self.pendulum.set_length(self.pendulum.length - 10)
        elif key == pygame.K_PLUS or key == pygame.K_EQUALS:
            self.pendulum.set_mass(self.pendulum.mass + 0.5)
        elif key == pygame.K_MINUS:
            self.pendulum.set_mass(self.pendulum.mass - 0.5)
        elif key == pygame.K_LEFT:
            self.pendulum.apply_impulse(-5.0)
        elif key == pygame.K_RIGHT:
            self.pendulum.apply_impulse(5.0)
        elif key == pygame.K_SPACE:
            self.pendulum.angular_velocity = 0.0
