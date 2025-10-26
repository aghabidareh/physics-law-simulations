import numpy as np
from config import (GAS_CONSTANT, MOLES, INITIAL_TEMPERATURE, ATMOSPHERIC_PRESSURE,
                    CYLINDER_WIDTH, CYLINDER_HEIGHT_MAX, CYLINDER_HEIGHT_MIN,
                    MAX_TEMPERATURE, MIN_TEMPERATURE, PISTON_MASS, GRAVITY,
                    NUM_PARTICLES, PARTICLE_RADIUS)


class GasParticle:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = PARTICLE_RADIUS


class GasSystem:
    def __init__(self, cylinder_x, cylinder_y, cylinder_width):
        self.cylinder_x = cylinder_x
        self.cylinder_y = cylinder_y
        self.cylinder_width = cylinder_width

        self.n = MOLES
        self.T = INITIAL_TEMPERATURE
        self.V = self._calculate_initial_volume()
        self.P = self._calculate_pressure()

        self.U = self._calculate_internal_energy()
        self.Q_total = 0.0
        self.W_total = 0.0

        self.initial_T = self.T
        self.initial_V = self.V
        self.initial_U = self.U

        self.piston_height = self._calculate_piston_height()
        self.piston_velocity = 0.0

        self.particles = self._initialize_particles()
        
    def _calculate_initial_volume(self):
        height_m = 0.2
        area_m2 = 0.015
        return height_m * area_m2
    
    def _calculate_pressure(self):
        if self.V > 0:
            return (self.n * GAS_CONSTANT * self.T) / self.V
        return ATMOSPHERIC_PRESSURE
    
    def _calculate_internal_energy(self):
        return 1.5 * self.n * GAS_CONSTANT * self.T
    
    def _calculate_piston_height(self):
        area_pixels = self.cylinder_width
        height_ratio = self.V / self.initial_V
        initial_height = 200
        height = initial_height * height_ratio
        return np.clip(height, CYLINDER_HEIGHT_MIN, CYLINDER_HEIGHT_MAX)
    
    def _initialize_particles(self):
        particles = []
        for _ in range(NUM_PARTICLES):
            x = self.cylinder_x + np.random.uniform(10, self.cylinder_width - 10)
            y = self.cylinder_y - np.random.uniform(10, self.piston_height - 10)

            speed = np.sqrt(self.T / 100)
            angle = np.random.uniform(0, 2 * np.pi)
            vx = speed * np.cos(angle)
            vy = speed * np.sin(angle)
            
            particles.append(GasParticle(x, y, vx, vy))
        return particles
    
    def add_heat(self, Q, dt):
        dQ = Q * dt
        self.Q_total += dQ

        dT = dQ / (1.5 * self.n * GAS_CONSTANT)
        self.T += dT
        self.T = np.clip(self.T, MIN_TEMPERATURE, MAX_TEMPERATURE)
        
        U_old = self.U
        self.U = self._calculate_internal_energy()
        
        self.P = self._calculate_pressure()
        
        self._update_particle_speeds()
    
    def update_piston(self, dt, external_force=0.0):
        area_m2 = 0.015
        F_pressure = (self.P - ATMOSPHERIC_PRESSURE) * area_m2
        F_gravity = -PISTON_MASS * GRAVITY
        F_net = F_pressure + F_gravity + external_force

        acceleration = F_net / PISTON_MASS
        self.piston_velocity += acceleration * dt
        
        self.piston_velocity *= 0.95
        
        old_height = self.piston_height
        self.piston_height += self.piston_velocity * dt * 100
        self.piston_height = np.clip(self.piston_height, CYLINDER_HEIGHT_MIN, CYLINDER_HEIGHT_MAX)

        old_V = self.V
        height_ratio = self.piston_height / 200.0
        self.V = self.initial_V * height_ratio
        dV = self.V - old_V

        if abs(dV) > 1e-10:
            dW = self.P * dV
            self.W_total += dW
            
            self.U -= dW
            
            if self.U > 0:
                self.T = self.U / (1.5 * self.n * GAS_CONSTANT)
                self.T = np.clip(self.T, MIN_TEMPERATURE, MAX_TEMPERATURE)
        
        self.P = self._calculate_pressure()
        
        self._update_particle_positions()
        self._update_particle_speeds()
    
    def compress_expand(self, force, dt):
        self.update_piston(dt, force)
    
    def _update_particle_speeds(self):
        speed = np.sqrt(self.T / 100)
        for p in self.particles:
            current_speed = np.sqrt(p.vx**2 + p.vy**2)
            if current_speed > 0:
                scale = speed / current_speed
                p.vx *= scale
                p.vy *= scale
    
    def _update_particle_positions(self):
        max_y = self.cylinder_y - self.piston_height
        for p in self.particles:
            if p.y < max_y:
                p.y = max_y + 5
    
    def update_particles(self, dt):
        for p in self.particles:
            p.x += p.vx * dt * 50
            p.y += p.vy * dt * 50

            if p.x <= self.cylinder_x or p.x >= self.cylinder_x + self.cylinder_width:
                p.vx *= -1
                p.x = np.clip(p.x, self.cylinder_x, self.cylinder_x + self.cylinder_width)
            
            if p.y >= self.cylinder_y:
                p.vy *= -1
                p.y = self.cylinder_y
            
            piston_y = self.cylinder_y - self.piston_height
            if p.y <= piston_y:
                p.vy *= -1
                p.y = piston_y
    
    def reset(self):
        self.T = self.initial_T
        self.V = self.initial_V
        self.U = self.initial_U
        self.P = self._calculate_pressure()
        self.piston_height = self._calculate_piston_height()
        self.piston_velocity = 0.0
        self.Q_total = 0.0
        self.W_total = 0.0
        self.particles = self._initialize_particles()
    
    def get_thermodynamic_state(self):
        return {
            'T': self.T,
            'P': self.P,
            'V': self.V,
            'U': self.U,
            'Q': self.Q_total,
            'W': self.W_total,
            'dU': self.U - self.initial_U
        }
