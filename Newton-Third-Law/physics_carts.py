import numpy as np
from config import CART_WIDTH, CART_HEIGHT, FRICTION_COEFFICIENT, GRAVITY


class PhysicsCart:
    def __init__(self, x, mass, color, width, height):
        self.width = width
        self.height = height
        self.ground_y = height - 100
        self.position = np.array([x, self.ground_y - CART_HEIGHT // 2], dtype=np.float64)
        self.velocity = np.array([0.0, 0.0], dtype=np.float64)
        self.width_cart = CART_WIDTH
        self.height_cart = CART_HEIGHT
        self.mass = mass
        self.color = color
        self.friction_coeff = FRICTION_COEFFICIENT
        self.force_during_collision = 0.0

    def update(self, dt):
        if abs(self.velocity[0]) > 0.01:
            friction_acceleration = self._calculate_friction_acceleration()
            self.velocity[0] += friction_acceleration * dt

            if abs(self.velocity[0]) < 0.05:
                self.velocity[0] = 0.0

        self.position[0] += self.velocity[0] * dt
        self._handle_boundary_collision()

    def _calculate_friction_acceleration(self):
        direction = -1 if self.velocity[0] > 0 else 1
        friction_force = direction * self.friction_coeff * self.mass * GRAVITY
        return friction_force / self.mass

    def _handle_boundary_collision(self):
        half_width = self.width_cart // 2
        if self.position[0] < half_width:
            self.position[0] = half_width
            self.velocity[0] = 0.0
        elif self.position[0] > self.width - half_width:
            self.position[0] = self.width - half_width
            self.velocity[0] = 0.0

    @staticmethod
    def handle_collision(cart1, cart2, dt):
        distance = cart2.position[0] - cart1.position[0]
        min_distance = cart1.width_cart

        if abs(distance) < min_distance:
            overlap = min_distance - abs(distance)

            stiffness = 500.0
            repulsion_force = overlap * stiffness

            force_direction = 1 if distance > 0 else -1
            force_on_cart1 = -force_direction * repulsion_force
            force_on_cart2 = force_direction * repulsion_force

            cart1.force_during_collision = force_on_cart1
            cart2.force_during_collision = force_on_cart2

            impulse1 = force_on_cart1 * dt
            impulse2 = force_on_cart2 * dt

            cart1.velocity[0] += impulse1 / cart1.mass
            cart2.velocity[0] += impulse2 / cart2.mass

            total_inv_mass = 1.0 / cart1.mass + 1.0 / cart2.mass
            correction = overlap / total_inv_mass
            cart1.position[0] -= force_direction * correction / cart1.mass
            cart2.position[0] += force_direction * correction / cart2.mass
        else:
            cart1.force_during_collision = 0.0
            cart2.force_during_collision = 0.0

    def set_velocity(self, v):
        self.velocity[0] = v

    def reset_position(self, x):
        self.position[0] = x
        self.velocity[0] = 0.0

    def get_momentum(self):
        return self.mass * self.velocity[0]

    def get_kinetic_energy(self):
        return 0.5 * self.mass * self.velocity[0] ** 2

    def get_force_arrow(self):
        if abs(self.force_during_collision) < 1:
            return None
        start = self.position + np.array([0, -50])
        end = start + np.array([self.force_during_collision * 0.05, 0])
        return start, end
