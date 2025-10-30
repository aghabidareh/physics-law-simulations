import numpy as np
from config import (MU_0, EPSILON_0, CURRENT_MIN, CURRENT_MAX,
                    LOOP_RADIUS_MIN, LOOP_RADIUS_MAX, FIELD_SCALE,
                    CAPACITOR_PLATE_WIDTH, CAPACITOR_PLATE_HEIGHT, CAPACITOR_GAP)


class CurrentWire:
    def __init__(self, x, y, current=0.0):
        self.position = np.array([float(x), float(y)], dtype=np.float64)
        self.current = np.clip(current, CURRENT_MIN, CURRENT_MAX)

    def set_position(self, x, y):
        self.position[:] = x, y

    def set_current(self, I):
        self.current = np.clip(I, CURRENT_MIN, CURRENT_MAX)

    def increase_current(self, step):
        self.current = np.clip(self.current + step, CURRENT_MIN, CURRENT_MAX)

    def decrease_current(self, step):
        self.current = np.clip(self.current - step, CURRENT_MIN, CURRENT_MAX)


class AmpereLoop:
    def __init__(self, x, y, radius):
        self.position = np.array([float(x), float(y)], dtype=np.float64)
        self.radius = np.clip(radius, LOOP_RADIUS_MIN, LOOP_RADIUS_MAX)
        self.enclosed_current = 0.0
        self.displacement_current = 0.0
        self.total_current = 0.0
        self.line_integral_B = 0.0

    def set_position(self, x, y):
        self.position[:] = x, y

    def set_radius(self, r):
        self.radius = np.clip(r, LOOP_RADIUS_MIN, LOOP_RADIUS_MAX)

    def calculate_enclosed_current(self, wires):
        self.enclosed_current = 0.0
        for wire in wires:
            distance = np.linalg.norm(self.position - wire.position)
            if distance < self.radius:
                self.enclosed_current += wire.current

    def calculate_displacement_current(self, capacitor):
        if capacitor is None:
            self.displacement_current = 0.0
            return

        distance = np.linalg.norm(self.position - capacitor.position)

        if distance + self.radius < CAPACITOR_GAP / 2:
            overlap_area = np.pi * self.radius ** 2
        elif distance > self.radius + CAPACITOR_GAP / 2:
            overlap_area = 0.0
        else:
            gap_center_x = capacitor.position[0]
            gap_y = capacitor.position[1]

            loop_intersects_gap = (
                abs(self.position[0] - gap_center_x) < self.radius and
                abs(self.position[1] - gap_y) < self.radius
            )

            if loop_intersects_gap:
                overlap_area = self._estimate_overlap_area(capacitor)
            else:
                overlap_area = 0.0

        dE_dt = capacitor.get_electric_field_rate()
        self.displacement_current = EPSILON_0 * overlap_area * dE_dt

    def _estimate_overlap_area(self, capacitor):
        gap_width = CAPACITOR_PLATE_WIDTH
        gap_height = CAPACITOR_GAP

        circle_area = np.pi * self.radius ** 2
        gap_area = gap_width * gap_height

        return min(circle_area, gap_area) * 0.5

    def update_ampere_law(self):
        self.total_current = self.enclosed_current + self.displacement_current
        self.line_integral_B = MU_0 * self.total_current


class Capacitor:
    def __init__(self, x, y):
        self.position = np.array([float(x), float(y)], dtype=np.float64)
        self.charge = 0.0
        self.max_charge = 10.0
        self.charge_rate = 0.0
        self.voltage = 0.0
        self.electric_field = 0.0
        self.previous_electric_field = 0.0
        self.is_charging = False

    def set_position(self, x, y):
        self.position[:] = x, y

    def set_charge_rate(self, rate):
        self.charge_rate = rate

    def start_charging(self):
        self.is_charging = True

    def stop_charging(self):
        self.is_charging = False
        self.charge_rate = 0.0

    def toggle_charging(self):
        self.is_charging = not self.is_charging
        if not self.is_charging:
            self.charge_rate = 0.0

    def update(self, dt):
        if self.is_charging:
            self.charge += self.charge_rate * dt
            self.charge = np.clip(self.charge, -self.max_charge, self.max_charge)

        area = CAPACITOR_PLATE_WIDTH * CAPACITOR_PLATE_HEIGHT / 10000.0
        capacitance = EPSILON_0 * area / (CAPACITOR_GAP / 1000.0)

        if capacitance > 0:
            self.voltage = self.charge / capacitance

        self.previous_electric_field = self.electric_field

        if CAPACITOR_GAP > 0:
            self.electric_field = self.voltage / (CAPACITOR_GAP / 1000.0)
        else:
            self.electric_field = 0.0

    def get_electric_field_rate(self):
        return self.charge_rate * 1000.0

    def reset(self):
        self.charge = 0.0
        self.charge_rate = 0.0
        self.voltage = 0.0
        self.electric_field = 0.0
        self.previous_electric_field = 0.0
        self.is_charging = False

    def get_plate_positions(self):
        left_plate_x = self.position[0] - CAPACITOR_GAP / 2
        right_plate_x = self.position[0] + CAPACITOR_GAP / 2

        return (
            np.array([left_plate_x, self.position[1]]),
            np.array([right_plate_x, self.position[1]])
        )


def calculate_magnetic_field(wires, point):
    B_total = np.zeros(2, dtype=np.float64)

    for wire in wires:
        r_vec = point - wire.position
        r = np.linalg.norm(r_vec)

        if r < 1e-6:
            continue

        B_magnitude = (MU_0 * abs(wire.current)) / (2 * np.pi * r) * FIELD_SCALE

        perp_direction = np.array([-r_vec[1], r_vec[0]]) / r

        if wire.current > 0:
            B_vec = B_magnitude * perp_direction
        else:
            B_vec = -B_magnitude * perp_direction

        B_total += B_vec

    return B_total


def calculate_line_integral(loop, wires):
    num_points = 64
    integral = 0.0

    for i in range(num_points):
        angle = 2 * np.pi * i / num_points
        next_angle = 2 * np.pi * (i + 1) / num_points

        point = loop.position + loop.radius * np.array([np.cos(angle), np.sin(angle)])
        next_point = loop.position + loop.radius * np.array([np.cos(next_angle), np.sin(next_angle)])

        dl = next_point - point

        B_field = calculate_magnetic_field(wires, point)

        integral += np.dot(B_field, dl)

    return integral


def sample_field_vectors(wires, width, height, spacing=80):
    vectors = []

    for x in range(spacing, width, spacing):
        for y in range(spacing, height, spacing):
            point = np.array([float(x), float(y)])
            B_field = calculate_magnetic_field(wires, point)

            if np.linalg.norm(B_field) > 1e-6:
                vectors.append((point, B_field))

    return vectors
