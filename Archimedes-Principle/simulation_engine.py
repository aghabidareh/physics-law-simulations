import asyncio
import pygame
from physics_buoyancy import FloatingObject, Fluid
from renderer import Renderer
from input_handler import InputHandler
from config import (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, LIGHT_BLUE, DARK_BLUE, ORANGE,
                    WATER_DENSITY, OIL_DENSITY, MERCURY_DENSITY)


class SimulationEngine:
    def __init__(self):
        pygame.init()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Archimedes' Principle Simulation")
        self.fps = FPS
        self.clock = pygame.time.Clock()
        self.running = True

        self.fluids = [
            Fluid(WATER_DENSITY, "Water", LIGHT_BLUE),
            Fluid(OIL_DENSITY, "Oil", ORANGE),
            Fluid(MERCURY_DENSITY, "Mercury", DARK_BLUE)
        ]
        self.current_fluid_index = 0
        self.current_fluid = self.fluids[self.current_fluid_index]

        self.objects = [
            FloatingObject(200, 100, 25, 500.0),
            FloatingObject(400, 100, 30, 1000.0),
            FloatingObject(600, 100, 35, 2000.0)
        ]

        self.renderer = Renderer(self.screen, self.width, self.height)
        self.input_handler = InputHandler(self.objects, self)

    def switch_fluid(self):
        self.current_fluid_index = (self.current_fluid_index + 1) % len(self.fluids)
        self.current_fluid = self.fluids[self.current_fluid_index]

    async def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            await asyncio.sleep(1.0 / self.fps)

    def handle_events(self):
        self.running = self.input_handler.process_events()

    def update(self):
        dt = 1.0 / self.fps
        for obj in self.objects:
            obj.update(dt, self.current_fluid.density, self.current_fluid.surface_y)

    def render(self):
        self.renderer.render(self.objects, self.current_fluid)
        self.clock.tick(self.fps)

    def cleanup(self):
        pygame.quit()
