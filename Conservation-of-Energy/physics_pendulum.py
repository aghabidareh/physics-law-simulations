import numpy as np
from config import (GRAVITY, AIR_RESISTANCE, DAMPING_FACTOR, 
                    PENDULUM_LENGTH_MIN, PENDULUM_LENGTH_MAX,
                    PENDULUM_MASS_MIN, PENDULUM_MASS_MAX, PENDULUM_RADIUS)


class Pendulum:
    def __init__(self, pivot_x, pivot_y, length, mass, colour):
        self.pivot = np.array([pivot_x, pivot_y], dtype=np.float64)
        self.length = length
        self.initial_length = length
        self.mass = mass
        self.initial_mass = mass
        self.colour = colour
        self.radius = PENDULUM_RADIUS
        
        self.angle = np.pi / 3
        self.initial_angle = self.angle
        self.angular_velocity = 0.0
        self.angular_acceleration = 0.0
        
        self.initial_total_energy = None
        
    def update(self, dt):
        self.angular_acceleration = -(GRAVITY / self.length) * np.sin(self.angle)
        
        air_resistance_torque = -AIR_RESISTANCE * self.angular_velocity * self.length ** 2
        self.angular_acceleration += air_resistance_torque / (self.mass * self.length ** 2)
        
        self.angular_velocity += self.angular_acceleration * dt
        self.angular_velocity *= DAMPING_FACTOR  # Apply damping
        self.angle += self.angular_velocity * dt
        
        if self.initial_total_energy is None:
            self.initial_total_energy = self.get_total_energy()
    
    def get_position(self):
        x = self.pivot[0] + self.length * np.sin(self.angle)
        y = self.pivot[1] + self.length * np.cos(self.angle)
        return np.array([x, y])
    
    def get_velocity(self):
        v = self.angular_velocity * self.length
        vx = v * np.cos(self.angle)
        vy = -v * np.sin(self.angle)
        return np.array([vx, vy])
    
    def get_height(self):
        lowest_y = self.pivot[1] + self.length
        current_y = self.get_position()[1]
        return lowest_y - current_y
    
    def get_potential_energy(self):
        h = self.get_height()
        return self.mass * GRAVITY * h
    
    def get_kinetic_energy(self):
        velocity = self.get_velocity()
        v_magnitude = np.linalg.norm(velocity)
        return 0.5 * self.mass * v_magnitude ** 2
    
    def get_total_energy(self):
        return self.get_potential_energy() + self.get_kinetic_energy()
    
    def set_angle(self, angle):
        self.angle = np.clip(angle, -np.pi * 0.9, np.pi * 0.9)
        self.angular_velocity = 0.0
        self.initial_total_energy = None
    
    def set_length(self, length):
        self.length = np.clip(length, PENDULUM_LENGTH_MIN, PENDULUM_LENGTH_MAX)
        self.initial_length = self.length
    
    def set_mass(self, mass):
        self.mass = np.clip(mass, PENDULUM_MASS_MIN, PENDULUM_MASS_MAX)
        self.initial_mass = self.mass
        self.initial_total_energy = None
    
    def reset(self):
        self.angle = self.initial_angle
        self.angular_velocity = 0.0
        self.angular_acceleration = 0.0
        self.length = self.initial_length
        self.mass = self.initial_mass
        self.initial_total_energy = None
    
    def apply_impulse(self, impulse):
        angular_impulse = impulse / (self.mass * self.length)
        self.angular_velocity += angular_impulse
        self.initial_total_energy = None
