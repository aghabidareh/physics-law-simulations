import numpy as np
from config import FRICTION_COEFFICIENT, GRAVITY, CART_HEIGHT, CART_WIDTH, CART_MASS_MIN, CART_MASS_MAX


class Cart:
    def __init__(self, x, mass, colour, width, height):
        self.width = width
        self.height = height
        self.ground_y = height - 100
        self.position = np.array([float(x), self.ground_y - CART_HEIGHT / 2], dtype=np.float64)
        self.velocity = np.zeros(2, dtype=np.float64)
        self.initial_mass = mass  # Store initial mass for reset
        self.mass = mass
        self.colour = colour
        self.radius = CART_WIDTH / 2          # for collision detection

    def apply_friction(self, dt):
        if abs(self.velocity[0]) < 1e-3:
            self.velocity[0] = 0.0
            return

        direction = -1 if self.velocity[0] > 0 else 1
        friction_force = direction * FRICTION_COEFFICIENT * self.mass * GRAVITY
        friction_acceleration = friction_force / self.mass

        new_velocity = self.velocity[0] + friction_acceleration * dt

        if new_velocity * direction > 0:
            self.velocity[0] = 0.0
        else:
            self.velocity[0] = new_velocity

    def update(self, dt):
        self.position += self.velocity * dt
        self._clamp_to_track()

    def _clamp_to_track(self):
        left = self.radius
        right = self.width - self.radius
        if self.position[0] < left:
            self.position[0] = left
            self.velocity[0] = 0.0
        elif self.position[0] > right:
            self.position[0] = right
            self.velocity[0] = 0.0

    def set_velocity(self, vx):
        self.velocity[0] = vx

    def set_mass(self, m):
        self.mass = np.clip(m, CART_MASS_MIN, CART_MASS_MAX)
        self.initial_mass = self.mass

    def reset(self, x):
        self.position[0] = x
        self.velocity[0] = 0.0
        self.mass = self.initial_mass

    def get_momentum(self):
        return self.mass * self.velocity[0]

    def get_kinetic_energy(self):
        return 0.5 * self.mass * self.velocity[0] ** 2

    @staticmethod
    def elastic_collision(c1, c2):
        m1, m2 = c1.mass, c2.mass
        v1, v2 = c1.velocity[0], c2.velocity[0]

        if (v1 - v2) * (c2.position[0] - c1.position[0]) < 0:
            return

        v1_final = (v1 * (m1 - m2) + 2 * m2 * v2) / (m1 + m2)
        v2_final = (v2 * (m2 - m1) + 2 * m1 * v1) / (m1 + m2)

        c1.velocity[0] = v1_final
        c2.velocity[0] = v2_final

    @staticmethod
    def inelastic_collision(c1, c2):
        v1, v2 = c1.velocity[0], c2.velocity[0]
        if (v1 - v2) * (c2.position[0] - c1.position[0]) < 0:
            return

        total_mass = c1.mass + c2.mass
        v_common = (c1.mass * v1 + c2.mass * v2) / total_mass

        c1.velocity[0] = v_common
        c2.velocity[0] = v_commonl