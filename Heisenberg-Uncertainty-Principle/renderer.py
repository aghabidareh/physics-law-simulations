import pygame
import numpy as np
from config import (WHITE, BLACK, BLUE, RED, GREEN, YELLOW, CYAN, GRAY,
                    LIGHT_BLUE, DARK_BLUE, GRAPH_MARGIN, GRAPH_HEIGHT,
                    GRAPH_SPACING, MEASUREMENT_DOT_SIZE)


class Renderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)
        self.font_large = pygame.font.Font(None, 32)

    def render(self, particle):
        self.screen.fill(BLACK)

        graph_y_start = 50
        self._render_position_graph(particle, graph_y_start)

        graph_y_start += GRAPH_HEIGHT + GRAPH_SPACING
        self._render_momentum_graph(particle, graph_y_start)

        self._render_uncertainty_info(particle)
        self._render_instructions()

        pygame.display.flip()

    def _render_position_graph(self, particle, y_start):
        graph_width = self.width - 2 * GRAPH_MARGIN
        graph_left = GRAPH_MARGIN
        graph_right = self.width - GRAPH_MARGIN
        graph_bottom = y_start + GRAPH_HEIGHT
        graph_center_y = y_start + GRAPH_HEIGHT // 2

        pygame.draw.line(self.screen, WHITE, (graph_left, graph_bottom),
                        (graph_right, graph_bottom), 2)
        pygame.draw.line(self.screen, WHITE, (graph_left, y_start),
                        (graph_left, graph_bottom), 2)

        label = self.font.render("Position Space Wave Function", True, CYAN)
        self.screen.blit(label, (graph_left, y_start - 30))

        if particle.wave_packet_x is not None and particle.wave_packet_prob is not None:
            x_vals = particle.wave_packet_x
            prob_vals = particle.wave_packet_prob

            x_min, x_max = x_vals[0], x_vals[-1]
            prob_max = np.max(prob_vals) if np.max(prob_vals) > 0 else 1.0

            points = []
            for i, (x, prob) in enumerate(zip(x_vals, prob_vals)):
                screen_x = graph_left + (x - x_min) / (x_max - x_min) * graph_width
                screen_y = graph_bottom - (prob / prob_max) * (GRAPH_HEIGHT - 20)
                points.append((screen_x, screen_y))

            if len(points) > 1:
                pygame.draw.lines(self.screen, LIGHT_BLUE, False, points, 2)

            if len(particle.position_measurements) > 0:
                for pos in particle.position_measurements:
                    if x_min <= pos <= x_max:
                        screen_x = graph_left + (pos - x_min) / (x_max - x_min) * graph_width
                        pygame.draw.circle(self.screen, RED, (int(screen_x), graph_bottom - 10),
                                         MEASUREMENT_DOT_SIZE)

        uncertainty_width = particle.position_uncertainty
        center_x = particle.mean_position
        left_x = center_x - uncertainty_width
        right_x = center_x + uncertainty_width

        if particle.wave_packet_x is not None:
            x_min, x_max = particle.wave_packet_x[0], particle.wave_packet_x[-1]
            if x_min <= left_x <= x_max and x_min <= right_x <= x_max:
                screen_left = graph_left + (left_x - x_min) / (x_max - x_min) * graph_width
                screen_right = graph_left + (right_x - x_min) / (x_max - x_min) * graph_width
                screen_center = graph_left + (center_x - x_min) / (x_max - x_min) * graph_width

                rect_height = 15
                rect_y = graph_bottom + 5
                pygame.draw.rect(self.screen, YELLOW,
                               (screen_left, rect_y, screen_right - screen_left, rect_height), 2)
                pygame.draw.line(self.screen, YELLOW, (screen_center, rect_y),
                               (screen_center, rect_y + rect_height), 2)

    def _render_momentum_graph(self, particle, y_start):
        graph_width = self.width - 2 * GRAPH_MARGIN
        graph_left = GRAPH_MARGIN
        graph_right = self.width - GRAPH_MARGIN
        graph_bottom = y_start + GRAPH_HEIGHT
        graph_center_y = y_start + GRAPH_HEIGHT // 2

        pygame.draw.line(self.screen, WHITE, (graph_left, graph_bottom),
                        (graph_right, graph_bottom), 2)
        pygame.draw.line(self.screen, WHITE, (graph_left, y_start),
                        (graph_left, graph_bottom), 2)

        label = self.font.render("Momentum Space Probability", True, GREEN)
        self.screen.blit(label, (graph_left, y_start - 30))

        if particle.momentum_space_p is not None and particle.momentum_space_prob is not None:
            p_vals = particle.momentum_space_p
            prob_vals = particle.momentum_space_prob

            p_min, p_max = p_vals[0], p_vals[-1]
            prob_max = np.max(prob_vals) if np.max(prob_vals) > 0 else 1.0

            points = []
            for i, (p, prob) in enumerate(zip(p_vals, prob_vals)):
                screen_x = graph_left + (p - p_min) / (p_max - p_min) * graph_width
                screen_y = graph_bottom - (prob / prob_max) * (GRAPH_HEIGHT - 20)
                points.append((screen_x, screen_y))

            if len(points) > 1:
                pygame.draw.lines(self.screen, GREEN, False, points, 2)

            if len(particle.momentum_measurements) > 0:
                for mom in particle.momentum_measurements:
                    if p_min <= mom <= p_max:
                        screen_x = graph_left + (mom - p_min) / (p_max - p_min) * graph_width
                        pygame.draw.circle(self.screen, RED, (int(screen_x), graph_bottom - 10),
                                         MEASUREMENT_DOT_SIZE)

        uncertainty_width = particle.momentum_uncertainty
        center_p = particle.mean_momentum
        left_p = center_p - uncertainty_width
        right_p = center_p + uncertainty_width

        if particle.momentum_space_p is not None:
            p_min, p_max = particle.momentum_space_p[0], particle.momentum_space_p[-1]
            if p_min <= left_p <= p_max and p_min <= right_p <= p_max:
                screen_left = graph_left + (left_p - p_min) / (p_max - p_min) * graph_width
                screen_right = graph_left + (right_p - p_min) / (p_max - p_min) * graph_width
                screen_center = graph_left + (center_p - p_min) / (p_max - p_min) * graph_width

                rect_height = 15
                rect_y = graph_bottom + 5
                pygame.draw.rect(self.screen, YELLOW,
                               (screen_left, rect_y, screen_right - screen_left, rect_height), 2)
                pygame.draw.line(self.screen, YELLOW, (screen_center, rect_y),
                               (screen_center, rect_y + rect_height), 2)

    def _render_uncertainty_info(self, particle):
        info_y = 480
        info_x = 50

        title = self.font_large.render("Heisenberg Uncertainty Principle", True, WHITE)
        self.screen.blit(title, (info_x, info_y))
        info_y += 40

        delta_x = particle.position_uncertainty
        delta_p = particle.momentum_uncertainty
        product = particle.get_uncertainty_product()
        limit = particle.get_heisenberg_limit()

        delta_x_text = self.font.render(f"Δx = {delta_x:.2f}", True, CYAN)
        self.screen.blit(delta_x_text, (info_x, info_y))
        info_y += 30

        delta_p_text = self.font.render(f"Δp = {delta_p:.2f}", True, GREEN)
        self.screen.blit(delta_p_text, (info_x, info_y))
        info_y += 30

        product_text = self.font.render(f"Δx · Δp = {product:.2f}", True, YELLOW)
        self.screen.blit(product_text, (info_x, info_y))
        info_y += 30

        limit_text = self.font.render(f"ℏ/2 = {limit:.2f}", True, WHITE)
        self.screen.blit(limit_text, (info_x, info_y))
        info_y += 30

        is_satisfied = particle.is_uncertainty_satisfied()
        if is_satisfied:
            status = self.font.render("✓ Uncertainty principle satisfied", True, GREEN)
        else:
            status = self.font.render("✗ Uncertainty principle violated", True, RED)
        self.screen.blit(status, (info_x, info_y))
        info_y += 35

        measured_x_std = particle.get_measured_position_std()
        measured_p_std = particle.get_measured_momentum_std()

        if measured_x_std is not None:
            measured_x_text = self.font_small.render(
                f"Measured Δx: {measured_x_std:.2f} ({len(particle.position_measurements)} samples)",
                True, CYAN)
            self.screen.blit(measured_x_text, (info_x, info_y))
        info_y += 25

        if measured_p_std is not None:
            measured_p_text = self.font_small.render(
                f"Measured Δp: {measured_p_std:.2f} ({len(particle.momentum_measurements)} samples)",
                True, GREEN)
            self.screen.blit(measured_p_text, (info_x, info_y))

    def _render_instructions(self):
        instructions_x = self.width - 350
        instructions_y = 480

        instructions = [
            "Controls:",
            "Q/W: Decrease/Increase Δx",
            "A/S: Decrease/Increase Δp",
            "SPACE: Measure position",
            "M: Measure momentum",
            "C: Clear measurements",
            "R: Reset",
            "ESC: Quit"
        ]

        for i, instruction in enumerate(instructions):
            if i == 0:
                text = self.font.render(instruction, True, WHITE)
            else:
                text = self.font_small.render(instruction, True, GRAY)
            self.screen.blit(text, (instructions_x, instructions_y + i * 22))
