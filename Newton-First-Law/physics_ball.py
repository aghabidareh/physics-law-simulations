import numpy as np
from config import (
    BALL_RADIUS, BALL_MASS, FRICTION_COEFFICIENT, GRAVITY,
    RESTITUTION, MIN_VELOCITY, INITIAL_VELOCITY_RANGE
)


class PhysicsBall:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = np.array([width / 2, height / 2], dtype=np.float64)
        self.velocity = np.array([0.0, 0.0], dtype=np.float64)
        self.radius = BALL_RADIUS
        self.mass = BALL_MASS
        self.friction_coeff = FRICTION_COEFFICIENT
        self.friction_enabled = False

    def update(self, dt):
        # Apply friction
        if self.friction_enabled:
            self._apply_friction(dt)

        self.position += self.velocity * dt

        self._handle_boundary_collision()

    def _apply_friction(self, dt):
        vel_squared = np.dot(self.velocity, self.velocity)
        if vel_squared < MIN_VELOCITY ** 2:
            self.velocity.fill(0.0)
            return

        vel_magnitude = np.sqrt(vel_squared)
        friction_force = self.friction_coeff * self.mass * GRAVITY
        friction_acceleration = friction_force / vel_magnitude

        new_velocity = self.velocity - (self.velocity / vel_magnitude) * friction_acceleration * dt

        if np.dot(new_velocity, self.velocity) < 0:
            self.velocity.fill(0.0)
        else:
            self.velocity = new_velocity

    def _handle_boundary_collision(self):
        if self.position[0] - self.radius < 0:
            self.position[0] = self.radius
            self.velocity[0] = -self.velocity[0] * RESTITUTION
        elif self.position[0] + self.radius > self.width:
            self.position[0] = self.width - self.radius
            self.velocity[0] = -self.velocity[0] * RESTITUTION

        if self.position[1] - self.radius < 0:
            self.position[1] = self.radius
            self.velocity[1] = -self.velocity[1] * RESTITUTION
        elif self.position[1] + self.radius > self.height:
            self.position[1] = self.height - self.radius
            self.velocity[1] = -self.velocity[1] * RESTITUTION

    def reset_with_random_velocity(self):
        self.position = np.array([self.width / 2, self.height / 2], dtype=np.float64)
        self.velocity = np.array([
            np.random.uniform(*INITIAL_VELOCITY_RANGE),
            np.random.uniform(*INITIAL_VELOCITY_RANGE)
        ], dtype=np.float64)

    def stop(self):
        self.velocity.fill(0.0)

    def toggle_friction(self):
        self.friction_enabled = not self.friction_enabled

    def get_color(self):
        return (255, 0, 0) if self.friction_enabled else (0, 0, 255)

    def get_kinetic_energy(self):
        vel_squared = np.dot(self.velocity, self.velocity)
        return 0.5 * self.mass * vel_squared