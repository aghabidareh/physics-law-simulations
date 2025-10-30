import numpy as np
from config import B_FIELD_MIN, B_FIELD_MAX, LOOP_RADIUS_MIN, LOOP_RADIUS_MAX


class ConductingLoop:
    def __init__(self, x, y, radius):
        self.position = np.array([float(x), float(y)], dtype=np.float64)
        self.radius = np.clip(radius, LOOP_RADIUS_MIN, LOOP_RADIUS_MAX)
        self.flux = 0.0
        self.previous_flux = 0.0
        self.emf = 0.0
        self.current = 0.0

    def set_position(self, x, y):
        self.position[:] = x, y

    def set_radius(self, r):
        self.radius = np.clip(r, LOOP_RADIUS_MIN, LOOP_RADIUS_MAX)

    def get_area(self):
        return np.pi * self.radius ** 2

    def update_flux(self, B_field_strength, field_region_center, field_region_radius):
        distance = np.linalg.norm(self.position - field_region_center)

        if distance + self.radius < field_region_radius:
            overlap_area = self.get_area()
        elif distance - self.radius > field_region_radius:
            overlap_area = 0.0
        else:
            overlap_area = self._calculate_circle_overlap(
                self.position, self.radius,
                field_region_center, field_region_radius
            )

        self.previous_flux = self.flux
        self.flux = B_field_strength * overlap_area

    def calculate_emf(self, dt):
        if dt > 0:
            d_flux = self.flux - self.previous_flux
            self.emf = -d_flux / dt
        else:
            self.emf = 0.0

        return self.emf

    def calculate_current(self, resistance=1.0):
        if resistance > 0:
            self.current = self.emf / resistance
        else:
            self.current = 0.0
        return self.current

    def _calculate_circle_overlap(self, pos1, r1, pos2, r2):
        d = np.linalg.norm(pos1 - pos2)

        if d >= r1 + r2:
            return 0.0
        if d <= abs(r1 - r2):
            return np.pi * min(r1, r2) ** 2

        d1 = (d**2 + r1**2 - r2**2) / (2 * d)
        d2 = d - d1

        if d1 < 0:
            d1 = 0
        if d2 < 0:
            d2 = 0

        if d1 > r1:
            d1 = r1
        if d2 > r2:
            d2 = r2

        area1 = r1**2 * np.arccos(d1/r1) if d1 < r1 else 0
        area2 = r2**2 * np.arccos(d2/r2) if d2 < r2 else 0
        area3 = 0.5 * np.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2)) if d > 0 else 0

        return area1 + area2 - area3


class MagneticFieldRegion:
    def __init__(self, x, y, radius, B_strength):
        self.position = np.array([float(x), float(y)], dtype=np.float64)
        self.radius = radius
        self.B_strength = np.clip(B_strength, B_FIELD_MIN, B_FIELD_MAX)
        self.velocity = np.zeros(2, dtype=np.float64)

    def set_position(self, x, y):
        self.position[:] = x, y

    def set_strength(self, B):
        self.B_strength = np.clip(B, B_FIELD_MIN, B_FIELD_MAX)

    def set_velocity(self, vx, vy):
        self.velocity[:] = vx, vy

    def update(self, dt):
        self.position += self.velocity * dt


class Magnet:
    def __init__(self, x, y, width, height, strength):
        self.position = np.array([float(x), float(y)], dtype=np.float64)
        self.width = width
        self.height = height
        self.strength = np.clip(strength, B_FIELD_MIN, B_FIELD_MAX)
        self.velocity = np.zeros(2, dtype=np.float64)

    def set_position(self, x, y):
        self.position[:] = x, y

    def set_velocity(self, vx, vy):
        self.velocity[:] = vx, vy

    def set_strength(self, s):
        self.strength = np.clip(s, B_FIELD_MIN, B_FIELD_MAX)

    def update(self, dt):
        self.position += self.velocity * dt

    def get_north_pole(self):
        return self.position + np.array([0, -self.height/2])

    def get_south_pole(self):
        return self.position + np.array([0, self.height/2])
