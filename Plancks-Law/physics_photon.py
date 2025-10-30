import numpy as np
from config import (PLANCK_CONSTANT, SPEED_OF_LIGHT, SCREEN_WIDTH, SCREEN_HEIGHT,
                    PHOTON_RADIUS, PHOTON_SPEED, SOURCE_X, SOURCE_Y,
                    WAVELENGTH_VISIBLE_MIN, WAVELENGTH_VISIBLE_MAX)


class Photon:
    def __init__(self, frequency):
        self.frequency = frequency
        self.energy = PLANCK_CONSTANT * frequency
        self.wavelength = SPEED_OF_LIGHT / frequency

        self.position = np.array([float(SOURCE_X), float(SOURCE_Y)], dtype=np.float64)
        angle = np.random.uniform(-np.pi / 6, np.pi / 6)
        self.velocity = np.array([
            PHOTON_SPEED * np.cos(angle),
            PHOTON_SPEED * np.sin(angle)
        ], dtype=np.float64)

        self.radius = PHOTON_RADIUS
        self.active = True
        self.color = self._wavelength_to_rgb()

    def _wavelength_to_rgb(self):
        wavelength = self.wavelength

        if wavelength < WAVELENGTH_VISIBLE_MIN or wavelength > WAVELENGTH_VISIBLE_MAX:
            intensity = self._calculate_intensity()
            gray = int(100 + 155 * intensity)
            return (gray, gray, gray)

        if wavelength < 440e-9:
            r = -(wavelength - 440e-9) / (440e-9 - 380e-9)
            g = 0.0
            b = 1.0
        elif wavelength < 490e-9:
            r = 0.0
            g = (wavelength - 440e-9) / (490e-9 - 440e-9)
            b = 1.0
        elif wavelength < 510e-9:
            r = 0.0
            g = 1.0
            b = -(wavelength - 510e-9) / (510e-9 - 490e-9)
        elif wavelength < 580e-9:
            r = (wavelength - 510e-9) / (580e-9 - 510e-9)
            g = 1.0
            b = 0.0
        elif wavelength < 645e-9:
            r = 1.0
            g = -(wavelength - 645e-9) / (645e-9 - 580e-9)
            b = 0.0
        else:
            r = 1.0
            g = 0.0
            b = 0.0

        factor = self._calculate_intensity()

        return (
            int(r * factor * 255),
            int(g * factor * 255),
            int(b * factor * 255)
        )

    def _calculate_intensity(self):
        wavelength = self.wavelength

        if wavelength >= WAVELENGTH_VISIBLE_MIN and wavelength <= WAVELENGTH_VISIBLE_MAX:
            return 1.0
        elif wavelength < WAVELENGTH_VISIBLE_MIN:
            if wavelength < 300e-9:
                return 0.4
            return 0.4 + 0.6 * (wavelength - 300e-9) / (WAVELENGTH_VISIBLE_MIN - 300e-9)
        else:
            if wavelength > 900e-9:
                return 0.4
            return 1.0 - 0.6 * (wavelength - WAVELENGTH_VISIBLE_MAX) / (900e-9 - WAVELENGTH_VISIBLE_MAX)

    def update(self, dt):
        if not self.active:
            return

        self.position += self.velocity * dt

        if (self.position[0] < 0 or self.position[0] > SCREEN_WIDTH or
            self.position[1] < 0 or self.position[1] > SCREEN_HEIGHT):
            self.active = False


class PhotonSource:
    def __init__(self):
        self.frequency = 5.5e14
        self.position = np.array([SOURCE_X, SOURCE_Y], dtype=np.float64)
        self.photons = []
        self.emission_timer = 0.0

    def get_energy(self):
        return PLANCK_CONSTANT * self.frequency

    def get_wavelength(self):
        return SPEED_OF_LIGHT / self.frequency

    def increase_frequency(self, amount):
        self.frequency = min(self.frequency + amount, 1.0e15)

    def decrease_frequency(self, amount):
        self.frequency = max(self.frequency - amount, 1.0e14)

    def set_frequency(self, freq):
        self.frequency = np.clip(freq, 1.0e14, 1.0e15)

    def emit_photon(self):
        photon = Photon(self.frequency)
        self.photons.append(photon)

    def update(self, dt, emission_interval):
        self.emission_timer += dt

        if self.emission_timer >= emission_interval:
            self.emit_photon()
            self.emission_timer = 0.0

        for photon in self.photons:
            photon.update(dt)

        self.photons = [p for p in self.photons if p.active]

    def clear_photons(self):
        self.photons.clear()
        self.emission_timer = 0.0


class SpectrumAnalyzer:
    @staticmethod
    def get_spectrum_type(wavelength):
        if wavelength < 10e-9:
            return "Gamma Ray"
        elif wavelength < 10e-6:
            return "X-Ray"
        elif wavelength < 380e-9:
            return "Ultraviolet"
        elif wavelength < 750e-9:
            return "Visible"
        elif wavelength < 1e-3:
            return "Infrared"
        elif wavelength < 1:
            return "Microwave"
        else:
            return "Radio Wave"

    @staticmethod
    def get_color_name(wavelength):
        if wavelength < 380e-9 or wavelength > 750e-9:
            return "Non-visible"
        elif wavelength < 450e-9:
            return "Violet"
        elif wavelength < 495e-9:
            return "Blue"
        elif wavelength < 570e-9:
            return "Green"
        elif wavelength < 590e-9:
            return "Yellow"
        elif wavelength < 620e-9:
            return "Orange"
        else:
            return "Red"
