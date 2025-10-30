import numpy as np
from config import EPSILON_0, FIELD_SCALE, CHARGE_RADIUS_MIN, CHARGE_RADIUS_MAX, CHARGE_MIN, CHARGE_MAX
from config import POSITIVE_COLOR, NEGATIVE_COLOR, NEUTRAL_COLOR, GAUSSIAN_SURFACE_RADIUS_MIN, GAUSSIAN_SURFACE_RADIUS_MAX


class Charge:
    def __init__(self, x, y, charge):
        self.charge = np.clip(charge, CHARGE_MIN, CHARGE_MAX)
        self.position = np.array([float(x), float(y)], dtype=np.float64)
        self.colour = self._colour_from_charge()
        self.radius = self._radius_from_charge()

    def _colour_from_charge(self):
        if abs(self.charge) < 1e-6:
            return NEUTRAL_COLOR
        elif self.charge > 0:
            return POSITIVE_COLOR
        else:
            return NEGATIVE_COLOR

    def _radius_from_charge(self):
        abs_charge = abs(self.charge)
        t = abs_charge / CHARGE_MAX
        return CHARGE_RADIUS_MIN + t * (CHARGE_RADIUS_MAX - CHARGE_RADIUS_MIN)

    def set_charge(self, q):
        self.charge = np.clip(q, CHARGE_MIN, CHARGE_MAX)
        self.colour = self._colour_from_charge()
        self.radius = self._radius_from_charge()

    def set_position(self, x, y):
        self.position[:] = x, y


class GaussianSurface:
    def __init__(self, x, y, radius):
        self.position = np.array([float(x), float(y)], dtype=np.float64)
        self.radius = np.clip(radius, GAUSSIAN_SURFACE_RADIUS_MIN, GAUSSIAN_SURFACE_RADIUS_MAX)

    def set_position(self, x, y):
        self.position[:] = x, y

    def set_radius(self, r):
        self.radius = np.clip(r, GAUSSIAN_SURFACE_RADIUS_MIN, GAUSSIAN_SURFACE_RADIUS_MAX)

    def is_charge_enclosed(self, charge):
        distance = np.linalg.norm(charge.position - self.position)
        return distance < self.radius


def calculate_electric_field(charges, point):
    E_total = np.zeros(2, dtype=np.float64)

    for charge in charges:
        r_vec = point - charge.position
        r_squared = np.dot(r_vec, r_vec)

        if r_squared < 1e-10:
            continue

        r = np.sqrt(r_squared)

        E_magnitude = (charge.charge / (4 * np.pi * EPSILON_0 * r_squared)) * FIELD_SCALE

        direction = r_vec / r
        E_total += E_magnitude * direction

    return E_total


def calculate_flux(surface, charges):
    enclosed_charges = []
    total_enclosed_charge = 0.0

    for charge in charges:
        if surface.is_charge_enclosed(charge):
            enclosed_charges.append(charge)
            total_enclosed_charge += charge.charge

    flux = total_enclosed_charge / EPSILON_0

    return flux, total_enclosed_charge, enclosed_charges


def sample_field_lines(charges, num_lines=16):
    field_lines = []

    for charge in charges:
        if abs(charge.charge) < 1e-6:
            continue

        sign = 1 if charge.charge > 0 else -1

        for i in range(num_lines):
            angle = 2 * np.pi * i / num_lines
            direction = np.array([np.cos(angle), np.sin(angle)])

            line_points = []
            current_pos = charge.position + direction * (charge.radius + 5)

            for step in range(50):
                line_points.append(current_pos.copy())

                E_field = calculate_electric_field(charges, current_pos)

                if np.linalg.norm(E_field) < 1e-6:
                    break

                E_normalized = E_field / np.linalg.norm(E_field)

                current_pos += sign * E_normalized * 5

                if (current_pos[0] < 0 or current_pos[0] > 1200 or
                    current_pos[1] < 0 or current_pos[1] > 900):
                    break

                for other_charge in charges:
                    if other_charge is not charge:
                        dist = np.linalg.norm(current_pos - other_charge.position)
                        if dist < other_charge.radius:
                            break

            if len(line_points) > 2:
                field_lines.append(line_points)

    return field_lines