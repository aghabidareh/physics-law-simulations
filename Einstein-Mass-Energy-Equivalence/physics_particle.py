import numpy as np
from config import (C_DISPLAY, PARTICLE_MASS_MIN, PARTICLE_MASS_MAX,
                    PARTICLE_RADIUS_MIN, PARTICLE_RADIUS_MAX, CONVERSION_DURATION,
                    PHOTON_COUNT, PHOTON_SPEED, PHOTON_RADIUS, KINETIC_VELOCITY_MAX)


class Particle:
    def __init__(self, x, y, mass):
        self.position = np.array([x, y], dtype=np.float64)
        self.rest_mass = np.clip(mass, PARTICLE_MASS_MIN, PARTICLE_MASS_MAX)
        self.velocity = np.zeros(2, dtype=np.float64)
        self.radius = self._radius_from_mass(self.rest_mass)
        self.converting = False
        self.conversion_progress = 0.0
        self.photons = []

    def _radius_from_mass(self, mass):
        t = (mass - PARTICLE_MASS_MIN) / (PARTICLE_MASS_MAX - PARTICLE_MASS_MIN)
        return PARTICLE_RADIUS_MIN + t * (PARTICLE_RADIUS_MAX - PARTICLE_RADIUS_MIN)

    def get_rest_energy(self):
        return self.rest_mass * C_DISPLAY ** 2

    def get_lorentz_factor(self):
        v_squared = np.dot(self.velocity, self.velocity)
        v = np.sqrt(v_squared)
        v_ratio = v / C_DISPLAY
        if v_ratio >= 1.0:
            v_ratio = 0.999
        return 1.0 / np.sqrt(1.0 - v_ratio ** 2)

    def get_relativistic_mass(self):
        gamma = self.get_lorentz_factor()
        return self.rest_mass * gamma

    def get_total_energy(self):
        gamma = self.get_lorentz_factor()
        return gamma * self.rest_mass * C_DISPLAY ** 2

    def get_kinetic_energy(self):
        return self.get_total_energy() - self.get_rest_energy()

    def set_mass(self, mass):
        self.rest_mass = np.clip(mass, PARTICLE_MASS_MIN, PARTICLE_MASS_MAX)
        self.radius = self._radius_from_mass(self.rest_mass)

    def set_velocity(self, vx, vy):
        self.velocity[0] = np.clip(vx, -KINETIC_VELOCITY_MAX * C_DISPLAY,
                                   KINETIC_VELOCITY_MAX * C_DISPLAY)
        self.velocity[1] = np.clip(vy, -KINETIC_VELOCITY_MAX * C_DISPLAY,
                                   KINETIC_VELOCITY_MAX * C_DISPLAY)

    def start_conversion(self):
        if not self.converting:
            self.converting = True
            self.conversion_progress = 0.0
            self._generate_photons()

    def _generate_photons(self):
        self.photons.clear()
        energy = self.get_rest_energy()
        for i in range(PHOTON_COUNT):
            angle = 2 * np.pi * i / PHOTON_COUNT
            photon = Photon(self.position[0], self.position[1], angle,
                          energy / PHOTON_COUNT)
            self.photons.append(photon)

    def reset_conversion(self):
        self.converting = False
        self.conversion_progress = 0.0
        self.photons.clear()

    def update(self, dt):
        if self.converting:
            self.conversion_progress += dt / CONVERSION_DURATION
            if self.conversion_progress > 1.0:
                self.conversion_progress = 1.0

            for photon in self.photons:
                photon.update(dt)


class Photon:
    def __init__(self, x, y, angle, energy):
        self.position = np.array([x, y], dtype=np.float64)
        self.angle = angle
        self.velocity = np.array([np.cos(angle), np.sin(angle)]) * PHOTON_SPEED
        self.energy = energy
        self.radius = PHOTON_RADIUS
        self.lifetime = 0.0

    def update(self, dt):
        self.position += self.velocity * dt
        self.lifetime += dt


class MassEnergySystem:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.particle = Particle(screen_width // 2, screen_height // 2, 10.0)
        self.mode = "rest"

    def set_rest_mass(self, mass):
        self.particle.set_mass(mass)

    def set_velocity_fraction(self, fraction):
        speed = fraction * C_DISPLAY * KINETIC_VELOCITY_MAX
        self.particle.set_velocity(speed, 0.0)

    def convert_mass_to_energy(self):
        self.mode = "conversion"
        self.particle.start_conversion()

    def reset(self):
        self.mode = "rest"
        self.particle.reset_conversion()
        self.particle.set_velocity(0.0, 0.0)

    def set_mode(self, mode):
        if mode != self.mode:
            self.mode = mode
            if mode == "rest":
                self.particle.set_velocity(0.0, 0.0)
                self.particle.reset_conversion()
            elif mode == "kinetic":
                self.particle.reset_conversion()
            elif mode == "conversion":
                self.convert_mass_to_energy()

    def update(self, dt):
        self.particle.update(dt)
