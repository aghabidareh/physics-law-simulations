import numpy as np
from config import K, COULOMB_SCALE, CHARGE_RADIUS_MIN, CHARGE_RADIUS_MAX, CHARGE_MIN, CHARGE_MAX
from config import POSITIVE_COLOR, NEGATIVE_COLOR, NEUTRAL_COLOR


class Charge:
    def __init__(self, x, y, charge, fixed=False):
        self.fixed = fixed
        self.charge = np.clip(charge, CHARGE_MIN, CHARGE_MAX)
        self.position = np.array([float(x), float(y)], dtype=np.float64)
        self.velocity = np.zeros(2, dtype=np.float64)
        self.force = np.zeros(2, dtype=np.float64)
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

    def reset_force(self):
        self.force.fill(0.0)

    def apply_force(self, f):
        self.force += f

    def update(self, dt):
        if self.fixed:
            return

        mass = abs(self.charge) if abs(self.charge) > 1e-6 else 1.0
        acceleration = self.force / mass
        self.velocity += acceleration * dt

        damping = 0.98
        self.velocity *= damping

        self.position += self.velocity * dt

    def set_charge(self, q):
        self.charge = np.clip(q, CHARGE_MIN, CHARGE_MAX)
        self.colour = self._colour_from_charge()
        self.radius = self._radius_from_charge()

    def set_position(self, x, y):
        self.position[:] = x, y
        self.velocity[:] = 0.0

    def set_velocity(self, vx, vy):
        self.velocity[:] = vx, vy

    def get_kinetic_energy(self):
        vel_squared = np.dot(self.velocity, self.velocity)
        mass = abs(self.charge) if abs(self.charge) > 1e-6 else 1.0
        return 0.5 * mass * vel_squared


def coulomb_force(c1: Charge, c2: Charge):
    r_vec = c2.position - c1.position
    r_squared = np.dot(r_vec, r_vec)

    if r_squared < 1e-10:
        return np.zeros(2, dtype=np.float64), np.zeros(2, dtype=np.float64)

    r = np.sqrt(r_squared)

    min_distance = c1.radius + c2.radius
    if r < min_distance:
        r = min_distance
        r_squared = r * r

    force_magnitude = (K * c1.charge * c2.charge / r_squared) * COULOMB_SCALE

    direction = r_vec / r

    force_on_c1 = force_magnitude * direction
    force_on_c2 = -force_on_c1

    return force_on_c1, force_on_c2


def calculate_system_energy(charges):
    kinetic_energy = sum(charge.get_kinetic_energy() for charge in charges)

    potential_energy = 0.0
    n = len(charges)
    for i in range(n):
        for j in range(i + 1, n):
            r_vec = charges[j].position - charges[i].position
            r = np.linalg.norm(r_vec)
            if r > 1e-10:
                potential_energy += (K * charges[i].charge * charges[j].charge / r) * COULOMB_SCALE

    return kinetic_energy, potential_energy, kinetic_energy + potential_energy