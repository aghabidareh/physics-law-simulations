import pygame
import numpy as np
from config import (WHITE, BLACK, BLUE, RED, GREEN, YELLOW, CYAN, MAGENTA,
                    ORANGE, PURPLE, GRAY, LIGHT_GRAY, LIGHT_BLUE, GOLD, C_DISPLAY)


class Renderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)
        self.font_large = pygame.font.Font(None, 36)
        self.font_title = pygame.font.Font(None, 48)

    def render(self, system):
        self.screen.fill(BLACK)

        if system.mode == "conversion":
            self._render_conversion_mode(system)
        else:
            self._render_particle(system.particle, system.mode)

        self._render_info_panel(system)
        self._render_mode_selector(system)
        self._render_instructions()

        pygame.display.flip()

    def _render_particle(self, particle, mode):
        pos_x, pos_y = int(particle.position[0]), int(particle.position[1])

        if mode == "kinetic":
            speed = np.linalg.norm(particle.velocity)
            if speed > 0.01:
                for i in range(3):
                    trail_alpha = 100 - i * 30
                    trail_radius = int(particle.radius * (1 - i * 0.15))
                    trail_offset = -particle.velocity / speed * i * 10
                    trail_pos = particle.position + trail_offset
                    color = tuple(int(c * (1 - i * 0.3)) for c in CYAN)
                    pygame.draw.circle(self.screen, color,
                                     (int(trail_pos[0]), int(trail_pos[1])),
                                     trail_radius, 2)

        color = BLUE if mode == "rest" else CYAN
        pygame.draw.circle(self.screen, color, (pos_x, pos_y), int(particle.radius))
        pygame.draw.circle(self.screen, WHITE, (pos_x, pos_y), int(particle.radius), 2)

        mass_text = self.font_small.render(f"m₀={particle.rest_mass:.1f}", True, WHITE)
        text_rect = mass_text.get_rect(center=(pos_x, pos_y))
        self.screen.blit(mass_text, text_rect)

    def _render_conversion_mode(self, system):
        particle = system.particle
        progress = particle.conversion_progress

        pos_x, pos_y = int(particle.position[0]), int(particle.position[1])

        if progress < 0.5:
            fade = 1.0 - (progress * 2)
            current_radius = int(particle.radius * fade)
            alpha_value = int(255 * fade)
            color = tuple(int(c * fade) for c in BLUE)

            if current_radius > 0:
                pygame.draw.circle(self.screen, color, (pos_x, pos_y), current_radius)
                border_color = tuple(int(c * fade) for c in WHITE)
                pygame.draw.circle(self.screen, border_color, (pos_x, pos_y),
                                 current_radius, 2)

        for photon in particle.photons:
            photon_alpha = min(1.0, progress * 2)
            if photon_alpha > 0:
                color = tuple(int(c * photon_alpha) for c in YELLOW)
                pygame.draw.circle(self.screen, color,
                                 (int(photon.position[0]), int(photon.position[1])),
                                 photon.radius)

                if photon.lifetime > 0:
                    angle = np.arctan2(photon.velocity[1], photon.velocity[0])
                    length = 15
                    end_x = photon.position[0] + np.cos(angle) * length
                    end_y = photon.position[1] + np.sin(angle) * length
                    pygame.draw.line(self.screen, ORANGE,
                                   (int(photon.position[0]), int(photon.position[1])),
                                   (int(end_x), int(end_y)), 2)

        if progress >= 0.3:
            glow_radius = int(particle.radius * 3 * (progress - 0.3) / 0.7)
            for r in range(glow_radius, 0, -5):
                alpha = int(50 * (1 - r / glow_radius))
                color = tuple(min(255, int(c + alpha)) for c in YELLOW)
                pygame.draw.circle(self.screen, color, (pos_x, pos_y), r, 1)

    def _render_info_panel(self, system):
        panel_x = 50
        panel_y = 50
        panel_width = 400
        panel_height = 280

        pygame.draw.rect(self.screen, GRAY,
                        (panel_x - 10, panel_y - 10, panel_width, panel_height), 2)

        title = self.font_large.render("E = mc²", True, GOLD)
        self.screen.blit(title, (panel_x, panel_y))
        y_offset = panel_y + 50

        particle = system.particle

        rest_mass_text = self.font.render(f"Rest Mass (m₀): {particle.rest_mass:.2f} units",
                                         True, WHITE)
        self.screen.blit(rest_mass_text, (panel_x, y_offset))
        y_offset += 30

        rest_energy = particle.get_rest_energy()
        rest_energy_text = self.font.render(f"Rest Energy (E₀): {rest_energy:.2f} units",
                                           True, BLUE)
        self.screen.blit(rest_energy_text, (panel_x, y_offset))
        y_offset += 35

        if system.mode == "kinetic":
            gamma = particle.get_lorentz_factor()
            gamma_text = self.font.render(f"Lorentz Factor (γ): {gamma:.4f}", True, CYAN)
            self.screen.blit(gamma_text, (panel_x, y_offset))
            y_offset += 30

            rel_mass = particle.get_relativistic_mass()
            rel_mass_text = self.font.render(f"Relativistic Mass: {rel_mass:.2f} units",
                                            True, CYAN)
            self.screen.blit(rel_mass_text, (panel_x, y_offset))
            y_offset += 30

            kinetic_energy = particle.get_kinetic_energy()
            kinetic_text = self.font.render(f"Kinetic Energy: {kinetic_energy:.2f} units",
                                           True, GREEN)
            self.screen.blit(kinetic_text, (panel_x, y_offset))
            y_offset += 30

            total_energy = particle.get_total_energy()
            total_text = self.font.render(f"Total Energy: {total_energy:.2f} units",
                                         True, YELLOW)
            self.screen.blit(total_text, (panel_x, y_offset))

        elif system.mode == "conversion":
            progress = particle.conversion_progress * 100
            progress_text = self.font.render(f"Conversion Progress: {progress:.0f}%",
                                            True, YELLOW)
            self.screen.blit(progress_text, (panel_x, y_offset))
            y_offset += 30

            photon_energy = rest_energy / len(particle.photons) if particle.photons else 0
            photon_text = self.font.render(f"Energy per Photon: {photon_energy:.2f} units",
                                          True, ORANGE)
            self.screen.blit(photon_text, (panel_x, y_offset))
            y_offset += 30

            total_text = self.font.render(f"Total Released: {rest_energy:.2f} units",
                                         True, GOLD)
            self.screen.blit(total_text, (panel_x, y_offset))

    def _render_mode_selector(self, system):
        mode_x = 550
        mode_y = 50

        title = self.font.render("Mode:", True, WHITE)
        self.screen.blit(title, (mode_x, mode_y))

        modes = [
            ("1: Rest Mass", "rest", BLUE),
            ("2: Kinetic Energy", "kinetic", CYAN),
            ("3: Mass → Energy", "conversion", YELLOW)
        ]

        y_offset = mode_y + 35
        for label, mode_name, color in modes:
            if system.mode == mode_name:
                pygame.draw.rect(self.screen, color,
                               (mode_x - 5, y_offset - 5, 200, 30), 2)
            text = self.font_small.render(label, True, color if system.mode == mode_name else GRAY)
            self.screen.blit(text, (mode_x, y_offset))
            y_offset += 35

    def _render_instructions(self):
        inst_x = 550
        inst_y = 250

        instructions = [
            ("Controls:", WHITE),
            ("1/2/3: Switch mode", LIGHT_GRAY),
            ("Q/W: Decrease/Increase mass", LIGHT_GRAY),
            ("A/S: Adjust velocity (kinetic mode)", LIGHT_GRAY),
            ("SPACE: Start conversion", LIGHT_GRAY),
            ("R: Reset", LIGHT_GRAY),
            ("ESC: Quit", LIGHT_GRAY)
        ]

        for i, (text, color) in enumerate(instructions):
            font = self.font if i == 0 else self.font_small
            rendered = font.render(text, True, color)
            self.screen.blit(rendered, (inst_x, inst_y + i * 25))
