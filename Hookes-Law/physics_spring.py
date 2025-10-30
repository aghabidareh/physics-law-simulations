import numpy as np
from config import (SPRING_K_MIN, SPRING_K_MAX, SPRING_K_DEFAULT,
                    MASS_MIN, MASS_MAX, MASS_DEFAULT,
                    DAMPING_MIN, DAMPING_MAX, DAMPING_DEFAULT,
                    GRAVITY, MASS_RADIUS, EQUILIBRIUM_Y, SPRING_ANCHOR_Y)


class SpringMassSystem:
    def __init__(self, x):
        self.anchor_x = x
        self.anchor_y = SPRING_ANCHOR_Y

        self.k = SPRING_K_DEFAULT
        self.mass = MASS_DEFAULT
        self.damping = DAMPING_DEFAULT
        self.gravity_enabled = True

        self.natural_length = EQUILIBRIUM_Y - SPRING_ANCHOR_Y
        self.equilibrium_position = self._calculate_equilibrium()

        self.position = np.array([float(x), self.equilibrium_position], dtype=np.float64)
        self.velocity = np.zeros(2, dtype=np.float64)
        self.force = np.zeros(2, dtype=np.float64)

        self.radius = MASS_RADIUS
        self.dragging = False

    def _calculate_equilibrium(self):
        if self.gravity_enabled:
            extension = (self.mass * GRAVITY) / self.k
            return self.anchor_y + self.natural_length + extension
        else:
            return self.anchor_y + self.natural_length

    def update(self, dt):
        if self.dragging:
            self.velocity.fill(0.0)
            return

        self.force.fill(0.0)

        displacement = self.position[1] - self.equilibrium_position

        spring_force = -self.k * displacement
        self.force[1] += spring_force

        damping_force = -self.damping * self.velocity
        self.force += damping_force

        acceleration = self.force / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt

        if self.position[1] < self.anchor_y + 10:
            self.position[1] = self.anchor_y + 10
            self.velocity[1] = 0

    def set_spring_constant(self, k):
        self.k = np.clip(k, SPRING_K_MIN, SPRING_K_MAX)
        self.equilibrium_position = self._calculate_equilibrium()

    def set_mass(self, m):
        self.mass = np.clip(m, MASS_MIN, MASS_MAX)
        self.equilibrium_position = self._calculate_equilibrium()

    def set_damping(self, d):
        self.damping = np.clip(d, DAMPING_MIN, DAMPING_MAX)

    def toggle_gravity(self):
        self.gravity_enabled = not self.gravity_enabled
        self.equilibrium_position = self._calculate_equilibrium()
        self.reset()

    def start_drag(self, mouse_pos):
        distance = np.linalg.norm(self.position - np.array(mouse_pos))
        if distance < self.radius + 5:
            self.dragging = True
            return True
        return False

    def drag_to(self, mouse_pos):
        if self.dragging:
            self.position[0] = self.anchor_x
            self.position[1] = float(mouse_pos[1])

    def end_drag(self):
        self.dragging = False

    def reset(self):
        self.equilibrium_position = self._calculate_equilibrium()
        self.position[1] = self.equilibrium_position
        self.position[0] = self.anchor_x
        self.velocity.fill(0.0)
        self.force.fill(0.0)

    def get_displacement(self):
        return self.position[1] - self.equilibrium_position

    def get_spring_force(self):
        displacement = self.get_displacement()
        return -self.k * displacement

    def get_potential_energy(self):
        displacement = self.get_displacement()
        spring_pe = 0.5 * self.k * displacement ** 2
        return spring_pe

    def get_kinetic_energy(self):
        vel_squared = np.dot(self.velocity, self.velocity)
        return 0.5 * self.mass * vel_squared

    def get_total_energy(self):
        return self.get_potential_energy() + self.get_kinetic_energy()

    def get_anchor_position(self):
        return np.array([self.anchor_x, self.anchor_y])
