import pygame
import numpy as np
from config import (WHITE, BLACK, GRAY, LIGHT_GRAY, DARK_GRAY, YELLOW,
                    SOURCE_X, SOURCE_Y, SOURCE_RADIUS, PLANCK_CONSTANT,
                    SPEED_OF_LIGHT, ENERGY_SCALE, FREQ_DISPLAY_SCALE)
from physics_photon import SpectrumAnalyzer


class Renderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(None, 28)
        self.title_font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 22)

    def render(self, photon_source, paused):
        self.screen.fill(BLACK)
        self.draw_source(photon_source)
        self.draw_photons(photon_source.photons)
        self.draw_info_panel(photon_source)
        self.draw_spectrum_bar(photon_source)
        self.draw_ui(photon_source, paused)
        pygame.display.flip()

    def draw_source(self, photon_source):
        pos = photon_source.position.astype(int)
        pygame.draw.circle(self.screen, YELLOW, pos, SOURCE_RADIUS)
        pygame.draw.circle(self.screen, WHITE, pos, SOURCE_RADIUS, 2)

        for i in range(8):
            angle = i * np.pi / 4
            start_x = pos[0] + int((SOURCE_RADIUS + 5) * np.cos(angle))
            start_y = pos[1] + int((SOURCE_RADIUS + 5) * np.sin(angle))
            end_x = pos[0] + int((SOURCE_RADIUS + 15) * np.cos(angle))
            end_y = pos[1] + int((SOURCE_RADIUS + 15) * np.sin(angle))
            pygame.draw.line(self.screen, YELLOW, (start_x, start_y), (end_x, end_y), 2)

    def draw_photons(self, photons):
        for photon in photons:
            if photon.active:
                pos = photon.position.astype(int)
                pygame.draw.circle(self.screen, photon.color, pos, photon.radius)
                pygame.draw.circle(self.screen, WHITE, pos, photon.radius, 1)

    def draw_info_panel(self, photon_source):
        panel_x = self.width - 380
        panel_y = 20
        panel_width = 360
        panel_height = 320

        pygame.draw.rect(self.screen, DARK_GRAY, (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(self.screen, WHITE, (panel_x, panel_y, panel_width, panel_height), 2)

        title = self.title_font.render("Planck's Law: E = hν", True, YELLOW)
        self.screen.blit(title, (panel_x + 10, panel_y + 10))

        frequency = photon_source.frequency
        energy = photon_source.get_energy()
        wavelength = photon_source.get_wavelength()

        info_lines = [
            "",
            f"Frequency (ν): {frequency * FREQ_DISPLAY_SCALE:.2f} × 10¹⁴ Hz",
            f"Energy (E): {energy * ENERGY_SCALE:.3f} × 10⁻¹⁹ J",
            f"Wavelength (λ): {wavelength * 1e9:.1f} nm",
            "",
            f"Planck's constant (h):",
            f"  {PLANCK_CONSTANT:.3e} J·s",
            "",
            f"Type: {SpectrumAnalyzer.get_spectrum_type(wavelength)}",
            f"Color: {SpectrumAnalyzer.get_color_name(wavelength)}",
        ]

        y_offset = 55
        for line in info_lines:
            if line:
                text = self.font.render(line, True, WHITE)
                self.screen.blit(text, (panel_x + 15, panel_y + y_offset))
            y_offset += 28

    def draw_spectrum_bar(self, photon_source):
        bar_x = 50
        bar_y = self.height - 120
        bar_width = self.width - 100
        bar_height = 40

        segments = 100
        segment_width = bar_width / segments

        for i in range(segments):
            freq = 1.0e14 + (1.0e15 - 1.0e14) * i / segments
            wavelength = SPEED_OF_LIGHT / freq

            if wavelength < 380e-9:
                color = (100, 100, 150)
            elif wavelength > 750e-9:
                color = (150, 100, 100)
            else:
                color = self._wavelength_to_rgb(wavelength)

            x = bar_x + i * segment_width
            pygame.draw.rect(self.screen, color, (x, bar_y, segment_width + 1, bar_height))

        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

        current_freq = photon_source.frequency
        marker_x = bar_x + (current_freq - 1.0e14) / (1.0e15 - 1.0e14) * bar_width
        marker_x = np.clip(marker_x, bar_x, bar_x + bar_width)

        pygame.draw.line(self.screen, WHITE, (marker_x, bar_y - 10), (marker_x, bar_y + bar_height + 10), 3)
        pygame.draw.circle(self.screen, YELLOW, (int(marker_x), bar_y - 15), 6)

        label = self.small_font.render("Electromagnetic Spectrum (1×10¹⁴ - 1×10¹⁵ Hz)", True, WHITE)
        self.screen.blit(label, (bar_x, bar_y - 35))

    def draw_ui(self, photon_source, paused):
        instructions = [
            "UP/DOWN: Adjust frequency | LEFT/RIGHT: Fine adjust",
            "SPACE: Pause/Resume | C: Clear photons | R: Reset | ESC: Quit",
            f"Active Photons: {len(photon_source.photons)}",
        ]

        if paused:
            instructions.append("*** PAUSED ***")

        for i, text in enumerate(instructions):
            color = YELLOW if "PAUSED" in text else LIGHT_GRAY
            rendered_text = self.small_font.render(text, True, color)
            self.screen.blit(rendered_text, (10, 10 + i * 25))

    def _wavelength_to_rgb(self, wavelength):
        if wavelength < 440e-9:
            r = -(wavelength - 440e-9) / (440e-9 - 380e-9)
            g = 0.0
            b = 1.0
        elif wavelength < 490e-9:
            r = 0.0
            g = (wavelength - 440e-9) / (490e-9 - 440e-9)
            b = 1.0
        elif wavelength < 510e-9:
            r = 0.0
            g = 1.0
            b = -(wavelength - 510e-9) / (510e-9 - 490e-9)
        elif wavelength < 580e-9:
            r = (wavelength - 510e-9) / (580e-9 - 510e-9)
            g = 1.0
            b = 0.0
        elif wavelength < 645e-9:
            r = 1.0
            g = -(wavelength - 645e-9) / (645e-9 - 580e-9)
            b = 0.0
        else:
            r = 1.0
            g = 0.0
            b = 0.0

        return (int(r * 255), int(g * 255), int(b * 255))
