import numpy as np


class PhysicsCart:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ground_y = height - 100  # Ground level
        self.position = np.array([width / 4, self.ground_y - 40], dtype=float)
        self.velocity = np.array([0.0, 0.0])
        self.width_cart = 80
        self.height_cart = 40
        self.mass = 2.0
        self.applied_force = 0.0  # Net external force in x-direction
        self.friction_coeff = 0.1
        self.friction_enabled = True

    def update(self, dt):
        # F_net = F_applied + F_friction
        friction_force = 0.0
        if self.friction_enabled and abs(self.velocity[0]) > 0.01:
            direction = -1 if self.velocity[0] > 0 else 1
            friction_force = direction * self.friction_coeff * self.mass * 9.81

        net_force_x = self.applied_force + friction_force
        acceleration_x = net_force_x / self.mass

        # Update velocity and position
        self.velocity[0] += acceleration_x * dt
        self.position[0] += self.velocity[0] * dt

        # Dampen small velocities
        if abs(self.velocity[0]) < 0.01:
            self.velocity[0] = 0.0

        self.handle_boundary_collision()

    def handle_boundary_collision(self):
        left = self.width_cart // 2
        right = self.width - self.width_cart // 2
        if self.position[0] - left < 0:
            self.position[0] = left
            self.velocity[0] = 0
        elif self.position[0] + left > self.width:
            self.position[0] = right
            self.velocity[0] = 0

    def set_force(self, force):
        self.applied_force = np.clip(force, -50, 50)

    def increase_force(self):
        self.applied_force = min(self.applied_force + 5, 50)

    def decrease_force(self):
        self.applied_force = max(self.applied_force - 5, -50)

    def increase_mass(self):
        self.mass = min(self.mass + 1.0, 10.0)

    def decrease_mass(self):
        self.mass = max(self.mass - 1.0, 1.0)

    def toggle_friction(self):
        self.friction_enabled = not self.friction_enabled

    def reset(self):
        self.position = np.array([self.width / 4, self.ground_y - 40], dtype=float)
        self.velocity = np.array([0.0, 0.0])
        self.applied_force = 0.0

    def get_color(self):
        return (0, 120, 215)  # Nice blue

    def get_force_arrow(self):
        start = self.position + np.array([0, -50])
        end = start + np.array([self.applied_force, 0])
        return start, end

    def get_acceleration(self):
        friction_force = 0.0
        if self.friction_enabled and abs(self.velocity[0]) > 0.01:
            direction = -1 if self.velocity[0] > 0 else 1
            friction_force = direction * self.friction_coeff * self.mass * 9.81
        net_force = self.applied_force + friction_force
        return net_force / self.mass
