import numpy as np


class PhysicsBall:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = np.array([width / 2, height / 2], dtype=float)
        self.velocity = np.array([0.0, 0.0])
        self.radius = 20
        self.mass = 1.0
        self.friction_coeff = 0.1
        self.friction_enabled = False

    def update(self):
        self.apply_friction()
        self.position += self.velocity
        self.handle_boundary_collision()

    def apply_friction(self):
        if not self.friction_enabled or np.linalg.norm(self.velocity) == 0:
            return

        vel_magnitude = np.linalg.norm(self.velocity)
        friction_dir = -self.velocity / vel_magnitude
        friction_force = self.friction_coeff * self.mass * 9.81 * friction_dir
        acceleration = friction_force / self.mass
        self.velocity += acceleration / 60

        if np.linalg.norm(self.velocity) < 0.1:
            self.velocity = np.array([0.0, 0.0])

    def handle_boundary_collision(self):
        if self.position[0] - self.radius < 0 or self.position[0] + self.radius > self.width:
            self.velocity[0] = -self.velocity[0]
            self.position[0] = np.clip(self.position[0], self.radius, self.width - self.radius)

        if self.position[1] - self.radius < 0 or self.position[1] + self.radius > self.height:
            self.velocity[1] = -self.velocity[1]
            self.position[1] = np.clip(self.position[1], self.radius, self.height - self.radius)

    def reset_with_random_velocity(self):
        self.position = np.array([self.width / 2, self.height / 2], dtype=float)
        self.velocity = np.array([
            np.random.uniform(-5, 5),
            np.random.uniform(-5, 5)
        ])

    def stop(self):
        self.velocity = np.array([0.0, 0.0])

    def toggle_friction(self):
        self.friction_enabled = not self.friction_enabled

    def get_color(self):
        return (255, 0, 0) if self.friction_enabled else (0, 0, 255)