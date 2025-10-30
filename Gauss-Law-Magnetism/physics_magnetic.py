import numpy as np
from config import MU_0, FIELD_SCALE, DIPOLE_MOMENT_MIN, DIPOLE_MOMENT_MAX, DIPOLE_LENGTH
from config import NORTH_COLOR, SOUTH_COLOR, GAUSSIAN_SURFACE_RADIUS_MIN, GAUSSIAN_SURFACE_RADIUS_MAX


class MagneticDipole:
    def __init__(self, x, y, moment, angle=0):
        self.position = np.array([float(x), float(y)], dtype=np.float64)
        self.moment = np.clip(moment, DIPOLE_MOMENT_MIN, DIPOLE_MOMENT_MAX)
        self.angle = angle
        self.length = DIPOLE_LENGTH

    def set_position(self, x, y):
        self.position[:] = x, y

    def set_moment(self, m):
        self.moment = np.clip(m, DIPOLE_MOMENT_MIN, DIPOLE_MOMENT_MAX)

    def set_angle(self, angle):
        self.angle = angle

    def rotate(self, delta_angle):
        self.angle += delta_angle

    def get_north_pole(self):
        direction = np.array([np.cos(self.angle), np.sin(self.angle)])
        return self.position + direction * self.length / 2

    def get_south_pole(self):
        direction = np.array([np.cos(self.angle), np.sin(self.angle)])
        return self.position - direction * self.length / 2


class GaussianSurface:
    def __init__(self, x, y, radius):
        self.position = np.array([float(x), float(y)], dtype=np.float64)
        self.radius = np.clip(radius, GAUSSIAN_SURFACE_RADIUS_MIN, GAUSSIAN_SURFACE_RADIUS_MAX)

    def set_position(self, x, y):
        self.position[:] = x, y

    def set_radius(self, r):
        self.radius = np.clip(r, GAUSSIAN_SURFACE_RADIUS_MIN, GAUSSIAN_SURFACE_RADIUS_MAX)

    def count_poles_enclosed(self, dipoles):
        north_count = 0
        south_count = 0

        for dipole in dipoles:
            north_pole = dipole.get_north_pole()
            south_pole = dipole.get_south_pole()

            dist_north = np.linalg.norm(north_pole - self.position)
            dist_south = np.linalg.norm(south_pole - self.position)

            if dist_north < self.radius:
                north_count += 1
            if dist_south < self.radius:
                south_count += 1

        return north_count, south_count


def calculate_magnetic_field(dipoles, point):
    B_total = np.zeros(2, dtype=np.float64)

    for dipole in dipoles:
        r_vec = point - dipole.position
        r = np.linalg.norm(r_vec)

        if r < 1e-10:
            continue

        m_vec = dipole.moment * np.array([np.cos(dipole.angle), np.sin(dipole.angle)])

        m_dot_r = np.dot(m_vec, r_vec)

        B = (MU_0 / (4 * np.pi * r**3)) * (3 * r_vec * m_dot_r / r**2 - m_vec)

        B_total += B * FIELD_SCALE

    return B_total


def calculate_flux(surface, dipoles):
    north_count, south_count = surface.count_poles_enclosed(dipoles)

    net_poles = north_count - south_count

    flux = 0.0

    flux_in = south_count
    flux_out = north_count

    return flux, net_poles, north_count, south_count, flux_in, flux_out


def sample_field_lines(dipoles, num_lines_per_pole=8):
    field_lines = []

    for dipole in dipoles:
        north_pole = dipole.get_north_pole()
        south_pole = dipole.get_south_pole()

        for i in range(num_lines_per_pole):
            angle = 2 * np.pi * i / num_lines_per_pole
            direction = np.array([np.cos(angle), np.sin(angle)])

            line_points = []
            current_pos = north_pole + direction * 5

            for step in range(100):
                line_points.append(current_pos.copy())

                B_field = calculate_magnetic_field(dipoles, current_pos)

                if np.linalg.norm(B_field) < 1e-6:
                    break

                B_normalized = B_field / np.linalg.norm(B_field)
                current_pos += B_normalized * 3

                if (current_pos[0] < 0 or current_pos[0] > 1200 or
                    current_pos[1] < 0 or current_pos[1] > 900):
                    break

                for other_dipole in dipoles:
                    dist_south = np.linalg.norm(current_pos - other_dipole.get_south_pole())
                    if dist_south < 10:
                        line_points.append(other_dipole.get_south_pole())
                        break

            if len(line_points) > 2:
                field_lines.append(line_points)

    return field_lines
