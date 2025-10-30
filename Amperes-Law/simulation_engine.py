import asyncio
import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from physics_ampere import CurrentWire, AmpereLoop, Capacitor
from input_handler import InputHandler
from renderer import Renderer


class SimulationEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Ampère's Law with Maxwell's Addition – ∮B·dl = μ₀(I + ε₀dΦ_E/dt)")
        self.clock = pygame.time.Clock()
        self.running = True

        self.wires = []
        self.loops = []
        self.capacitor = Capacitor(600, 450)

        self.renderer = Renderer(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.input = InputHandler(self.wires, self.loops, self.capacitor)

        self._create_default_scene()
        self.dt = 1.0 / FPS

    def _create_default_scene(self):
        self.wires.clear()
        self.loops.clear()

        self.wires.append(CurrentWire(400, 450, current=3.0))
        self.wires.append(CurrentWire(600, 450, current=-2.0))

        self.loops.append(AmpereLoop(500, 450, radius=150))
        self.loops.append(AmpereLoop(600, 300, radius=100))

    async def run(self):
        while self.running:
            self.running = self.input.process_events()
            self._update()
            self._render()
            self.clock.tick(FPS)
            await asyncio.sleep(0)

    def _update(self):
        self.capacitor.update(self.dt)

        for loop in self.loops:
            if self.input.show_mode == 'wire':
                loop.calculate_enclosed_current(self.wires)
                loop.displacement_current = 0.0
            else:
                loop.enclosed_current = 0.0
                loop.calculate_displacement_current(self.capacitor)

            loop.update_ampere_law()

    def _render(self):
        self.renderer.render(
            self.wires,
            self.loops,
            self.capacitor,
            self.input.selected_loop,
            self.input.show_mode
        )

    def cleanup(self):
        pygame.quit()
