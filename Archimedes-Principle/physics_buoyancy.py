import numpy as np
from config import (GRAVITY, FLUID_SURFACE_Y, FLUID_HEIGHT, FLUID_DRAG_COEFFICIENT,
                    OBJECT_RADIUS_MIN, OBJECT_RADIUS_MAX,
                    OBJECT_DENSITY_MIN, OBJECT_DENSITY_MAX,
                    SCREEN_HEIGHT)


class FloatingObject:
    def __init__(self, x, y, radius, density):
        self.position = np.array([float(x), float(y)], dtype=np.float64)
        self.velocity = np.zeros(2, dtype=np.float64)
        self.acceleration = np.zeros(2, dtype=np.float64)

        self.radius = np.clip(radius, OBJECT_RADIUS_MIN, OBJECT_RADIUS_MAX)
        self.density = np.clip(density, OBJECT_DENSITY_MIN, OBJECT_DENSITY_MAX)

        self.dragging = False

    def get_volume(self):
        return (4.0 / 3.0) * np.pi * (self.radius ** 3)

    def get_mass(self):
        return self.density * self.get_volume()

    def get_submerged_volume(self, fluid_surface_y):
        fluid_bottom = fluid_surface_y + FLUID_HEIGHT

        if self.position[1] + self.radius < fluid_surface_y:
            return 0.0

        if self.position[1] - self.radius > fluid_bottom:
            return 0.0

        if self.position[1] - self.radius >= fluid_surface_y and self.position[1] + self.radius <= fluid_bottom:
            return self.get_volume()

        top = max(self.position[1] - self.radius, fluid_surface_y)
        bottom = min(self.position[1] + self.radius, fluid_bottom)

        if bottom <= top:
            return 0.0

        h1 = self.position[1] - top
        h2 = bottom - self.position[1]

        if h1 < 0:
            h1 = 0
        if h2 < 0:
            h2 = 0

        r = self.radius

        cap_volume_top = 0
        if h1 < r:
            cap_volume_top = np.pi * h1 ** 2 * (3 * r - h1) / 3
        else:
            cap_volume_top = self.get_volume()

        cap_volume_bottom = 0
        if h2 < r:
            cap_volume_bottom = np.pi * h2 ** 2 * (3 * r - h2) / 3
        else:
            cap_volume_bottom = self.get_volume()

        if self.position[1] < fluid_surface_y:
            return cap_volume_bottom
        elif self.position[1] > fluid_bottom:
            return cap_volume_top
        else:
            return min(cap_volume_top + cap_volume_bottom, self.get_volume())

    def is_in_fluid(self, fluid_surface_y):
        fluid_bottom = fluid_surface_y + FLUID_HEIGHT
        return self.position[1] + self.radius > fluid_surface_y and self.position[1] - self.radius < fluid_bottom

    def update(self, dt, fluid_density, fluid_surface_y):
        if self.dragging:
            self.velocity.fill(0.0)
            return

        self.acceleration.fill(0.0)

        gravity_force = self.get_mass() * GRAVITY
        self.acceleration[1] += gravity_force / self.get_mass()

        submerged_volume = self.get_submerged_volume(fluid_surface_y)

        if submerged_volume > 0:
            buoyant_force = fluid_density * submerged_volume * GRAVITY
            self.acceleration[1] -= buoyant_force / self.get_mass()

            if self.is_in_fluid(fluid_surface_y):
                drag_force = FLUID_DRAG_COEFFICIENT * self.velocity
                self.acceleration -= drag_force

        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

        fluid_bottom = fluid_surface_y + FLUID_HEIGHT
        if self.position[1] + self.radius > SCREEN_HEIGHT:
            self.position[1] = SCREEN_HEIGHT - self.radius
            self.velocity[1] = 0

        if self.position[0] - self.radius < 0:
            self.position[0] = self.radius
            self.velocity[0] *= -0.5
        elif self.position[0] + self.radius > 800:
            self.position[0] = 800 - self.radius
            self.velocity[0] *= -0.5

    def set_radius(self, r):
        self.radius = np.clip(r, OBJECT_RADIUS_MIN, OBJECT_RADIUS_MAX)

    def set_density(self, d):
        self.density = np.clip(d, OBJECT_DENSITY_MIN, OBJECT_DENSITY_MAX)

    def start_drag(self, mouse_pos):
        distance = np.linalg.norm(self.position - np.array(mouse_pos))
        if distance < self.radius + 5:
            self.dragging = True
            return True
        return False

    def drag_to(self, mouse_pos):
        if self.dragging:
            self.position[:] = mouse_pos

    def end_drag(self):
        self.dragging = False

    def get_color(self):
        ratio = (self.density - OBJECT_DENSITY_MIN) / (OBJECT_DENSITY_MAX - OBJECT_DENSITY_MIN)
        ratio = np.clip(ratio, 0, 1)

        r = int(220 * ratio + 50 * (1 - ratio))
        g = int(50 * ratio + 200 * (1 - ratio))
        b = int(50 * ratio + 200 * (1 - ratio))

        return (r, g, b)

    def get_buoyant_force(self, fluid_density, fluid_surface_y):
        submerged_volume = self.get_submerged_volume(fluid_surface_y)
        return fluid_density * submerged_volume * GRAVITY

    def get_weight(self):
        return self.get_mass() * GRAVITY


class Fluid:
    def __init__(self, density, name, color):
        self.density = density
        self.name = name
        self.color = color
        self.surface_y = FLUID_SURFACE_Y
