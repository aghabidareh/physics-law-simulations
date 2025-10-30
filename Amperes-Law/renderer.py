import numpy as np
import pygame

from config import (WIRE_COLOR, CURRENT_COLOR, LOOP_COLOR, B_FIELD_COLOR,
                    E_FIELD_COLOR, CAPACITOR_PLATE_COLOR, POSITIVE_CHARGE_COLOR,
                    NEGATIVE_CHARGE_COLOR, FONT_NAME, FONT_SIZE, WIRE_RADIUS,
                    CAPACITOR_PLATE_WIDTH, CAPACITOR_PLATE_HEIGHT, CAPACITOR_GAP)
from physics_ampere import sample_field_vectors


class Renderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.small_font = pygame.font.SysFont(FONT_NAME, 18)

    def render(self, wires, loops, capacitor, selected_loop, show_mode):
        self.screen.fill((10, 10, 20))

        if show_mode == 'wire':
            self._draw_field_vectors(wires)
            self._draw_wires(wires)
            self._draw_loops(loops, selected_loop)
        elif show_mode == 'capacitor':
            self._draw_capacitor(capacitor)
            self._draw_capacitor_fields(capacitor)
            self._draw_loops(loops, selected_loop)

        self._draw_ui(wires, loops, capacitor, selected_loop, show_mode)

        pygame.display.flip()

    def _draw_wires(self, wires):
        for wire in wires:
            center = wire.position.astype(int)

            color_intensity = min(255, int(abs(wire.current) * 20))
            wire_color = (color_intensity, color_intensity // 2, 0) if wire.current != 0 else WIRE_COLOR

            pygame.draw.circle(self.screen, wire_color, center, WIRE_RADIUS)
            pygame.draw.circle(self.screen, (255, 255, 255), center, WIRE_RADIUS, 2)

            if abs(wire.current) > 0.1:
                if wire.current > 0:
                    size = 15
                    pygame.draw.circle(self.screen, CURRENT_COLOR, center, 4, 0)
                    pygame.draw.line(self.screen, CURRENT_COLOR,
                                   (center[0] - size, center[1]), (center[0] + size, center[1]), 3)
                    pygame.draw.line(self.screen, CURRENT_COLOR,
                                   (center[0], center[1] - size), (center[0], center[1] + size), 3)
                else:
                    radius = 12
                    pygame.draw.circle(self.screen, CURRENT_COLOR, center, radius, 3)
                    size = 8
                    pygame.draw.line(self.screen, CURRENT_COLOR,
                                   (center[0] - size, center[1] - size), (center[0] + size, center[1] + size), 3)
                    pygame.draw.line(self.screen, CURRENT_COLOR,
                                   (center[0] - size, center[1] + size), (center[0] + size, center[1] - size), 3)

                current_txt = self.small_font.render(f"I={wire.current:.1f}A", True, CURRENT_COLOR)
                self.screen.blit(current_txt, (center[0] + 20, center[1] - 30))

    def _draw_loops(self, loops, selected_loop):
        for loop in loops:
            center = loop.position.astype(int)
            radius = int(loop.radius)

            thickness = 4 if loop is selected_loop else 3
            color = (255, 255, 0) if loop is selected_loop else LOOP_COLOR

            pygame.draw.circle(self.screen, color, center, radius, thickness)

            I_enc_txt = self.small_font.render(f"I_enc={loop.enclosed_current:.2f}A", True, (200, 200, 255))
            I_disp_txt = self.small_font.render(f"I_disp={loop.displacement_current:.2f}A", True, (255, 200, 100))
            B_txt = self.small_font.render(f"∮B·dl={loop.line_integral_B:.2e}", True, B_FIELD_COLOR)

            self.screen.blit(I_enc_txt, (center[0] - 60, center[1] - 35))
            self.screen.blit(I_disp_txt, (center[0] - 60, center[1] - 15))
            self.screen.blit(B_txt, (center[0] - 60, center[1] + 5))

    def _draw_field_vectors(self, wires):
        vectors = sample_field_vectors(wires, self.width, self.height, spacing=80)

        for point, B_field in vectors:
            B_magnitude = np.linalg.norm(B_field)

            if B_magnitude < 1e-6:
                continue

            max_arrow_length = 30
            arrow_length = min(B_magnitude * 0.5, max_arrow_length)

            B_direction = B_field / B_magnitude

            start = point
            end = point + B_direction * arrow_length

            pygame.draw.line(self.screen, B_FIELD_COLOR,
                           start.astype(int), end.astype(int), 2)

            arrow_size = 6
            angle = np.arctan2(B_direction[1], B_direction[0])
            p1 = end - arrow_size * np.array([np.cos(angle - 0.5), np.sin(angle - 0.5)])
            p2 = end - arrow_size * np.array([np.cos(angle + 0.5), np.sin(angle + 0.5)])
            pygame.draw.polygon(self.screen, B_FIELD_COLOR,
                              [end.astype(int), p1.astype(int), p2.astype(int)])

    def _draw_capacitor(self, capacitor):
        left_plate, right_plate = capacitor.get_plate_positions()

        left_rect = pygame.Rect(
            int(left_plate[0] - 10),
            int(left_plate[1] - CAPACITOR_PLATE_HEIGHT / 2),
            20,
            CAPACITOR_PLATE_HEIGHT
        )
        right_rect = pygame.Rect(
            int(right_plate[0] - 10),
            int(right_plate[1] - CAPACITOR_PLATE_HEIGHT / 2),
            20,
            CAPACITOR_PLATE_HEIGHT
        )

        left_color = POSITIVE_CHARGE_COLOR if capacitor.charge > 0 else NEGATIVE_CHARGE_COLOR if capacitor.charge < 0 else CAPACITOR_PLATE_COLOR
        right_color = NEGATIVE_CHARGE_COLOR if capacitor.charge > 0 else POSITIVE_CHARGE_COLOR if capacitor.charge < 0 else CAPACITOR_PLATE_COLOR

        pygame.draw.rect(self.screen, left_color, left_rect)
        pygame.draw.rect(self.screen, right_color, right_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), left_rect, 2)
        pygame.draw.rect(self.screen, (255, 255, 255), right_rect, 2)

        if abs(capacitor.charge) > 0.1:
            left_label = "+" if capacitor.charge > 0 else "-"
            right_label = "-" if capacitor.charge > 0 else "+"

            left_txt = self.font.render(left_label, True, (255, 255, 255))
            right_txt = self.font.render(right_label, True, (255, 255, 255))

            self.screen.blit(left_txt, (left_rect.centerx - 8, left_rect.centery - 12))
            self.screen.blit(right_txt, (right_rect.centerx - 8, right_rect.centery - 12))

        charge_txt = self.small_font.render(f"Q={capacitor.charge:.2f}C", True, (200, 255, 200))
        voltage_txt = self.small_font.render(f"V={capacitor.voltage:.2f}V", True, (200, 255, 200))
        E_txt = self.small_font.render(f"E={capacitor.electric_field:.2e}V/m", True, E_FIELD_COLOR)

        center = capacitor.position.astype(int)
        self.screen.blit(charge_txt, (center[0] - 40, center[1] - 120))
        self.screen.blit(voltage_txt, (center[0] - 40, center[1] - 100))
        self.screen.blit(E_txt, (center[0] - 60, center[1] - 80))

    def _draw_capacitor_fields(self, capacitor):
        if abs(capacitor.electric_field) < 1e-6:
            return

        left_plate, right_plate = capacitor.get_plate_positions()

        num_lines = 10
        for i in range(num_lines):
            offset = (i - num_lines / 2 + 0.5) * 15
            y = capacitor.position[1] + offset

            if abs(y - capacitor.position[1]) < CAPACITOR_PLATE_HEIGHT / 2:
                if capacitor.charge > 0:
                    start = (int(left_plate[0]), int(y))
                    end = (int(right_plate[0]), int(y))
                else:
                    start = (int(right_plate[0]), int(y))
                    end = (int(left_plate[0]), int(y))

                pygame.draw.line(self.screen, E_FIELD_COLOR, start, end, 1)

                arrow_size = 4
                pygame.draw.polygon(self.screen, E_FIELD_COLOR, [
                    end,
                    (end[0] - arrow_size * (1 if capacitor.charge > 0 else -1), end[1] - arrow_size),
                    (end[0] - arrow_size * (1 if capacitor.charge > 0 else -1), end[1] + arrow_size)
                ])

    def _draw_ui(self, wires, loops, capacitor, selected_loop, show_mode):
        lines = [
            "Ampère's Law with Maxwell's Addition",
            "∮B·dl = μ₀(I_enc + I_disp)",
            "",
        ]

        if show_mode == 'wire':
            lines.extend([
                "MODE: Current Wire",
                "Left-click wire → select | Drag wire → move",
                "Right-click → add wire",
                "UP/DOWN → increase/decrease current",
                "+ / − → change loop radius",
                "TAB → switch to capacitor mode",
                "",
                f"Wires: {len(wires)} | Loops: {len(loops)}",
            ])
        else:
            lines.extend([
                "MODE: Charging Capacitor",
                "SPACE → start/stop charging",
                "UP/DOWN → increase/decrease charge rate",
                "TAB → switch to wire mode",
                "",
                f"Charging: {capacitor.is_charging} | Rate: {capacitor.charge_rate:.2f}",
            ])

        lines.extend([
            "",
            "R → reset | ESC → deselect",
        ])

        if selected_loop:
            lines.append(f"SELECTED LOOP: radius={selected_loop.radius:.0f}")
        else:
            lines.append("No selection")

        for i, txt in enumerate(lines):
            if i == 0:
                col = (255, 200, 0)
            elif i < 10:
                col = (200, 200, 200)
            else:
                col = (150, 255, 150)

            surf = self.font.render(txt, True, col)
            self.screen.blit(surf, (15, 15 + i * (FONT_SIZE + 4)))
