import asyncio
import pygame
from config import (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BODY1_X, BODY2_X, BODY_Y,
                    BODY_WIDTH, BODY_HEIGHT, TEMP_HOT_INITIAL, TEMP_COLD_INITIAL,
                    THERMAL_CONDUCTIVITY, RED, BLUE)
from physics_thermal import ThermalBody, HeatTransferSystem
from renderer import Renderer
from input_handler import InputHandler


class SimulationEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Second Law of Thermodynamics - Heat Transfer")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create thermal bodies
        self.body1 = ThermalBody(
            BODY1_X, BODY_Y, BODY_WIDTH, BODY_HEIGHT,
            TEMP_HOT_INITIAL, "Body 1", RED
        )
        self.body2 = ThermalBody(
            BODY2_X, BODY_Y, BODY_WIDTH, BODY_HEIGHT,
            TEMP_COLD_INITIAL, "Body 2", BLUE
        )
        
        # Create heat transfer system
        self.heat_system = HeatTransferSystem(
            self.body1, self.body2, THERMAL_CONDUCTIVITY
        )
        
        self.renderer = Renderer(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.input_handler = InputHandler(self.heat_system)
        
        self.dt = 1.0 / FPS
    
    async def run(self):
        while self.running:
            self.running = self.input_handler.process_events()
            self._step()
            self.renderer.render(self.heat_system, self.input_handler)
            self.clock.tick(FPS)
            await asyncio.sleep(0)
    
    def _step(self):
        """Update physics simulation"""
        # Update based on user input
        self.input_handler.update(self.dt)
        
        # Update heat transfer
        self.heat_system.update(self.dt)
    
    def cleanup(self):
        pygame.quit()
