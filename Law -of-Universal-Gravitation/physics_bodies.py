import numpy as np
from config import G, GRAVITY_SCALE, BODY_RADIUS_MIN, BODY_RADIUS_MAX, MASS_MIN, MASS_MAX

class Body:
    def __init__(self, x, y, mass, colour, fixed=False):
        self.fixed = fixed
        self.mass = np.clip(mass, MASS_MIN, MASS_MAX)
        self.position = np.array([float(x), float(y)], dtype=np.float64)
        self.velocity = np.zeros(2, dtype=np.float64)
        self.force = np.zeros(2, dtype=np.float64)
        self.colour = colour
        self.radius = self._radius_from_mass()

    def _radius_from_mass(self):
        # Visual radius grows with log(mass)
        log_m = np.log10(self.mass)
        log_min, log_max = np.log10(MASS_MIN), np.log10(MASS_MAX)
        t = (log_m - log_min) / (log_max - log_min)
        return BODY_RADIUS_MIN + t * (BODY_RADIUS_MAX - BODY_RADIUS_MIN)

    def reset_force(self):
        self.force.fill(0.0)

    def apply_force(self, f):
        self.force += f

    def update(self, dt):
        if self.fixed:
            return
        acc = self.force / self.mass
        self.velocity += acc * dt
        self.position += self.velocity * dt

    def set_mass(self, m):
        self.mass = np.clip(m, MASS_MIN, MASS_MAX)
        self.radius = self._radius_from_mass()

    def set_position(self, x, y):
        self.position[:] = x, y
        self.velocity[:] = 0.0

    def set_velocity(self, vx, vy):
        self.velocity[:] = vx, vy


def gravitational_force(b1: Body, b2: Body):
    """Return (force on b1, force on b2) – equal magnitude, opposite direction."""
    r_vec = b2.position - b1.position
    r2 = np.dot(r_vec, r_vec)

    if r2 == 0:
        return np.zeros(2), np.zeros(2)

    # Avoid division by zero / tiny distances
    r = np.sqrt(r2)
    if r < b1.radius + b2.radius:
        r = b1.radius + b2.radius

    F = G * b1.mass * b2.mass / (r * r) * GRAVITY_SCALE
    direction = r_vec / r
    f1 = F * direction
    f2 = -f1
    return f1, f2