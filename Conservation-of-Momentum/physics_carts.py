import numpy as np
from config import FRICTION_COEFFICIENT, GRAVITY, CART_HEIGHT, CART_WIDTH, CART_MASS_MIN, CART_MASS_MAX


class Cart:
    def __init__(self, x, mass, colour, width, height):
        self.width = width
        self.height = height
        self.ground_y = height - 100
        self.position = np.array([float(x), self.ground_y - CART_HEIGHT/2], dtype=np.float64)
        self.velocity = np.zeros(2, dtype=np.float64)
        self.mass = mass
        self.colour = colour
        self.radius = CART_WIDTH / 2          # for collision detection

    # ------------------------------------------------------------------
    def apply_friction(self, dt):
        if abs(self.velocity[0]) < 1e-3:
            self.velocity[0] = 0.0
            return
        direction = -1 if self.velocity[0] > 0 else 1
        f_fric = direction * FRICTION_COEFFICIENT * self.mass * GRAVITY
        acc = f_fric / self.mass
        self.velocity[0] += acc * dt
        if self.velocity[0] * direction > 0:      # still moving opposite to friction?
            self.velocity[0] = 0.0

    # ------------------------------------------------------------------
    def update(self, dt):
        self.position += self.velocity * dt
        self._clamp_to_track()

    def _clamp_to_track(self):
        left  = self.radius
        right = self.width - self.radius
        if self.position[0] < left:
            self.position[0] = left
            self.velocity[0] = 0.0
        elif self.position[0] > right:
            self.position[0] = right
            self.velocity[0] = 0.0

    # ------------------------------------------------------------------
    def set_velocity(self, vx):
        self.velocity[0] = vx

    def set_mass(self, m):
        self.mass = max(CART_MASS_MIN, min(CART_MASS_MAX, m))

    def reset(self, x):
        self.position[0] = x
        self.velocity[0] = 0.0

    # ------------------------------------------------------------------
    @staticmethod
    def elastic_collision(c1, c2):
        """Perfectly elastic 1-D collision – momentum & KE conserved."""
        m1, m2 = c1.mass, c2.mass
        v1, v2 = c1.velocity[0], c2.velocity[0]

        # Classic formulas
        v1f = (v1 * (m1 - m2) + 2 * m2 * v2) / (m1 + m2)
        v2f = (v2 * (m2 - m1) + 2 * m1 * v1) / (m1 + m2)

        c1.velocity[0] = v1f
        c2.velocity[0] = v2f

    @staticmethod
    def inelastic_collision(c1, c2):
        """Perfectly inelastic – they stick together."""
        total_m = c1.mass + c2.mass
        v_common = (c1.mass * c1.velocity[0] + c2.mass * c2.velocity[0]) / total_m
        c1.velocity[0] = v_common
        c2.velocity[0] = v_common
        # merge masses
        c1.mass = total_m
        c2.mass = total_m