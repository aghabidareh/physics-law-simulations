import numpy as np


class PhysicsCart:
    def __init__(self, x, mass, color, width, height):
        self.width = width
        self.height = height
        self.ground_y = height - 100
        self.position = np.array([x, self.ground_y - 40], dtype=float)
        self.velocity = np.array([0.0, 0.0])
        self.width_cart = 80
        self.height_cart = 40
        self.mass = mass
        self.color = color
        self.friction_coeff = 0.05
        self.force_during_collision = 0.0  # For visualization

    def update(self, dt, other_cart=None):
        # Apply friction
        if abs(self.velocity[0]) > 0.01:
            direction = -1 if self.velocity[0] > 0 else 1
            friction = direction * self.friction_coeff * self.mass * 9.81

            self.velocity[0] += friction * dt / self.mass

            # Dampen small velocities
            if abs(self.velocity[0]) < 0.05:
                self.velocity[0] = 0.0

            self.position[0] += self.velocity[0] * dt
            self.handle_boundary_collision()
            self.force_during_collision = 0.0  # Reset

            if other_cart:
                self.handle_collision(other_cart, dt)

    def handle_boundary_collision(self):
        left = self.width_cart // 2
        right = self.width - self.width_cart // 2
        if self.position[0] - left < 0:
            self.position[0] = left
            self.velocity[0] = 0
        elif self.position[0] + left > self.width:
            self.position[0] = right
            self.velocity[0] = 0

    def handle_collision(self, other, dt):
        dist = abs(self.position[0] - other.position[0])
        min_dist = self.width_cart

        if dist < min_dist and (
                (self.velocity[0] > other.velocity[0]) or abs(self.velocity[0] - other.velocity[0]) > 0.1):
            # Collision detected
            overlap = min_dist - dist
            push = overlap * 200  # Spring-like force

            # Action-reaction: equal and opposite
            force = push
            self.force_during_collision = force
            other.force_during_collision = -force

            # Apply impulse
            inv_mass1 = 1.0 / self.mass
            inv_mass2 = 1.0 / other.mass
            total_inv_mass = inv_mass1 + inv_mass2

            impulse = force * dt
            self.velocity[0] += impulse * inv_mass1
            other.velocity[0] -= impulse * inv_mass2

            # Separate carts
            correction = overlap / total_inv_mass
            self.position[0] += correction * inv_mass1
            other.position[0] -= correction * inv_mass2

    def set_velocity(self, v):
        self.velocity[0] = v

    def reset_position(self, x):
        self.position[0] = x
        self.velocity[0] = 0.0

    def get_momentum(self):
        return self.mass * self.velocity[0]

    def get_force_arrow(self):
        if abs(self.force_during_collision) < 1:
            return None
        start = self.position + np.array([0, -50])
        end = start + np.array([self.force_during_collision * 0.1, 0])
        return start, end
