import numpy as np
from config import (HBAR_DISPLAY, MIN_UNCERTAINTY, POSITION_UNCERTAINTY_MIN,
                    POSITION_UNCERTAINTY_MAX, MOMENTUM_UNCERTAINTY_MIN,
                    MOMENTUM_UNCERTAINTY_MAX, WAVE_PACKET_POINTS, GAUSSIAN_WIDTH,
                    MEASUREMENT_POINTS)


class QuantumParticle:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.position_uncertainty = 10.0
        self.momentum_uncertainty = HBAR_DISPLAY / (2 * self.position_uncertainty)

        self.mean_position = 0.0
        self.mean_momentum = 0.0

        self.position_measurements = []
        self.momentum_measurements = []

        self.measuring_position = False
        self.measuring_momentum = False

        self.wave_packet_x = None
        self.wave_packet_psi_real = None
        self.wave_packet_psi_imag = None
        self.wave_packet_prob = None

        self.momentum_space_p = None
        self.momentum_space_prob = None

        self._generate_wave_packets()

    def _generate_wave_packets(self):
        x_range = GAUSSIAN_WIDTH * self.position_uncertainty
        self.wave_packet_x = np.linspace(-x_range, x_range, WAVE_PACKET_POINTS)

        gaussian = np.exp(-(self.wave_packet_x - self.mean_position)**2 /
                         (2 * self.position_uncertainty**2))
        phase = np.exp(1j * self.mean_momentum * self.wave_packet_x / HBAR_DISPLAY)
        wave_function = gaussian * phase

        norm = np.sqrt(np.trapz(np.abs(wave_function)**2, self.wave_packet_x))
        wave_function /= norm

        self.wave_packet_psi_real = np.real(wave_function)
        self.wave_packet_psi_imag = np.imag(wave_function)
        self.wave_packet_prob = np.abs(wave_function)**2

        p_range = GAUSSIAN_WIDTH * self.momentum_uncertainty
        self.momentum_space_p = np.linspace(-p_range, p_range, WAVE_PACKET_POINTS)

        momentum_gaussian = np.exp(-(self.momentum_space_p - self.mean_momentum)**2 /
                                   (2 * self.momentum_uncertainty**2))
        norm_p = np.sqrt(np.trapz(momentum_gaussian**2, self.momentum_space_p))
        momentum_gaussian /= norm_p

        self.momentum_space_prob = momentum_gaussian**2

    def set_position_uncertainty(self, delta_x):
        self.position_uncertainty = np.clip(delta_x,
                                           POSITION_UNCERTAINTY_MIN,
                                           POSITION_UNCERTAINTY_MAX)
        self.momentum_uncertainty = HBAR_DISPLAY / (2 * self.position_uncertainty)
        self._generate_wave_packets()
        self.clear_measurements()

    def set_momentum_uncertainty(self, delta_p):
        self.momentum_uncertainty = np.clip(delta_p,
                                           MOMENTUM_UNCERTAINTY_MIN,
                                           MOMENTUM_UNCERTAINTY_MAX)
        self.position_uncertainty = HBAR_DISPLAY / (2 * self.momentum_uncertainty)
        self._generate_wave_packets()
        self.clear_measurements()

    def measure_position(self):
        self.measuring_position = True
        position = np.random.normal(self.mean_position, self.position_uncertainty)
        self.position_measurements.append(position)
        if len(self.position_measurements) > MEASUREMENT_POINTS:
            self.position_measurements.pop(0)
        return position

    def measure_momentum(self):
        self.measuring_momentum = True
        momentum = np.random.normal(self.mean_momentum, self.momentum_uncertainty)
        self.momentum_measurements.append(momentum)
        if len(self.momentum_measurements) > MEASUREMENT_POINTS:
            self.momentum_measurements.pop(0)
        return momentum

    def clear_measurements(self):
        self.position_measurements.clear()
        self.momentum_measurements.clear()

    def get_uncertainty_product(self):
        return self.position_uncertainty * self.momentum_uncertainty

    def get_heisenberg_limit(self):
        return MIN_UNCERTAINTY

    def is_uncertainty_satisfied(self):
        return self.get_uncertainty_product() >= self.get_heisenberg_limit()

    def get_measured_position_std(self):
        if len(self.position_measurements) < 2:
            return None
        return np.std(self.position_measurements)

    def get_measured_momentum_std(self):
        if len(self.momentum_measurements) < 2:
            return None
        return np.std(self.momentum_measurements)

    def update(self, dt):
        self.measuring_position = False
        self.measuring_momentum = False
