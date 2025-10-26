import numpy as np
from config import (
    CART_WIDTH, CART_HEIGHT, INITIAL_MASS,
    FRICTION_COEFFICIENT, GRAVITY, CART_MASS_MIN, CART_MASS_MAX
)


class PhysicsCart:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ground_y = height - 100
        self.position = np.array([width / 4, self.ground_y - CART_HEIGHT // 2], dtype=np.float64)
        self.velocity = np.array([0.0, 0.0], dtype=np.float64)
        self.width_cart = CART_WIDTH
        self.height_cart = CART_HEIGHT
        self.mass = INITIAL_MASS
        self.applied_force = 0.0
        self.friction_coeff = FRICTION_COEFFICIENT
        self.friction_enabled = True

        self._cached_acceleration = 0.0
        self._cached_friction_force = 0.0

    def update(self, dt):
        self._cached_friction_force = self._calculate_friction_force()
        net_force_x = self.applied_force + self._cached_friction_force
        self._cached_acceleration = net_force_x / self.mass

        self.velocity[0] += self._cached_acceleration * dt
        self.position[0] += self.velocity[0] * dt

        if abs(self.velocity[0]) < 0.01:
            self.velocity[0] = 0.0

        self._handle_boundary_collision()

    def _calculate_friction_force(self):
        if not self.friction_enabled or abs(self.velocity[0]) < 0.01:
            return 0.0

        direction = -1 if self.velocity[0] > 0 else 1
        return direction * self.friction_coeff * self.mass * GRAVITY

    def _handle_boundary_collision(self):
        half_width = self.width_cart // 2
        if self.position[0] < half_width:
            self.position[0] = half_width
            self.velocity[0] = 0.0
        elif self.position[0] > self.width - half_width:
            self.position[0] = self.width - half_width
            self.velocity[0] = 0.0

    def set_force(self, force):
        from config import FORCE_MAX
        self.applied_force = np.clip(force, -FORCE_MAX, FORCE_MAX)

    def increase_force(self):
        from config import FORCE_MAX, FORCE_STEP
        self.applied_force = min(self.applied_force + FORCE_STEP, FORCE_MAX)

    def decrease_force(self):
        from config import FORCE_MAX, FORCE_STEP
        self.applied_force = max(self.applied_force - FORCE_STEP, -FORCE_MAX)

    def increase_mass(self):
        self.mass = min(self.mass + 1.0, CART_MASS_MAX)

    def decrease_mass(self):
        self.mass = max(self.mass - 1.0, CART_MASS_MIN)

    def toggle_friction(self):
        self.friction_enabled = not self.friction_enabled

    def reset(self):
        self.position = np.array([self.width / 4, self.ground_y - self.height_cart // 2], dtype=np.float64)
        self.velocity.fill(0.0)
        self.applied_force = 0.0

    def get_color(self):
        return (0, 120, 215)  # Nice blue

    def get_force_arrow(self):
        start = self.position + np.array([0, -50])
        end = start + np.array([self.applied_force, 0])
        return start, end

    def get_acceleration(self):
        return self._cached_acceleration

    def get_kinetic_energy(self):
        return 0.5 * self.mass * self.velocity[0] ** 2
