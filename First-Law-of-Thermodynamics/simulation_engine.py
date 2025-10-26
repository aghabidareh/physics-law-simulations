import asyncio
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, CYLINDER_X, CYLINDER_Y, CYLINDER_WIDTH
from physics_gas import GasSystem
from renderer import Renderer
from input_handler import InputHandler


class SimulationEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("First Law of Thermodynamics - Piston-Cylinder System")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.gas = GasSystem(CYLINDER_X, CYLINDER_Y, CYLINDER_WIDTH)
        
        self.renderer = Renderer(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.input_handler = InputHandler(self.gas)
        
        self.dt = 1.0 / FPS
    
    async def run(self):
        while self.running:
            self.running = self.input_handler.process_events()
            self._step()
            self.renderer.render(self.gas, self.input_handler)
            self.clock.tick(FPS)
            await asyncio.sleep(0)
    
    def _step(self):
        self.input_handler.update(self.dt)
        
        if not self.input_handler.compressing and not self.input_handler.expanding:
            self.gas.update_piston(self.dt)
        
        self.gas.update_particles(self.dt)
    
    def cleanup(self):
        pygame.quit()
