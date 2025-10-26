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

        acceleration = self.force / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt

    def set_mass(self, m):
        self.mass = np.clip(m, MASS_MIN, MASS_MAX)
        self.radius = self._radius_from_mass()

    def set_position(self, x, y):
        self.position[:] = x, y
        self.velocity[:] = 0.0

    def set_velocity(self, vx, vy):
        self.velocity[:] = vx, vy

    def get_kinetic_energy(self):
        vel_squared = np.dot(self.velocity, self.velocity)
        return 0.5 * self.mass * vel_squared

    def get_momentum(self):
        return self.mass * self.velocity


def gravitational_force(b1: Body, b2: Body):
    r_vec = b2.position - b1.position
    r_squared = np.dot(r_vec, r_vec)

    if r_squared < 1e-10:
        return np.zeros(2, dtype=np.float64), np.zeros(2, dtype=np.float64)

    r = np.sqrt(r_squared)

    min_distance = b1.radius + b2.radius
    if r < min_distance:
        r = min_distance
        r_squared = r * r

    force_magnitude = (G * b1.mass * b2.mass / r_squared) * GRAVITY_SCALE

    direction = r_vec / r

    force_on_b1 = force_magnitude * direction
    force_on_b2 = -force_on_b1

    return force_on_b1, force_on_b2


def calculate_system_energy(bodies):
    kinetic_energy = sum(body.get_kinetic_energy() for body in bodies)

    potential_energy = 0.0
    n = len(bodies)
    for i in range(n):
        for j in range(i + 1, n):
            r_vec = bodies[j].position - bodies[i].position
            r = np.linalg.norm(r_vec)
            if r > 1e-10:
                potential_energy -= (G * bodies[i].mass * bodies[j].mass / r) * GRAVITY_SCALE

    return kinetic_energy, potential_energy, kinetic_energy + potential_energy
