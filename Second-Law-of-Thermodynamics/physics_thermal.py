import numpy as np
from config import (SPECIFIC_HEAT, MASS, T_REFERENCE, TEMP_MIN, TEMP_MAX,
                    NUM_FLOW_PARTICLES, PARTICLE_RADIUS)


class HeatFlowParticle:
    """Represents a heat flow particle for visualization"""
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.progress = 0.0  # 0 to 1
        self.radius = PARTICLE_RADIUS
        self.active = True


class ThermalBody:
    """Represents a thermal body with temperature and entropy"""
    
    def __init__(self, x, y, width, height, initial_temp, name, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.T = initial_temp  # Temperature in Kelvin
        self.initial_T = initial_temp
        self.name = name
        self.color = color
        
        self.mass = MASS
        self.specific_heat = SPECIFIC_HEAT
        
        self.S = self._calculate_entropy()
        self.initial_S = self.S
        
        self.Q_absorbed = 0.0  # Total heat absorbed (can be negative)
        
    def _calculate_entropy(self):
        """Calculate entropy using S = m*c*ln(T/T_ref)"""
        if self.T > 0 and T_REFERENCE > 0:
            return self.mass * self.specific_heat * np.log(self.T / T_REFERENCE)
        return 0.0
    
    def add_heat(self, dQ):
        """Add heat to the body (dQ can be negative for heat loss)"""
        self.Q_absorbed += dQ
        
        dT = dQ / (self.mass * self.specific_heat)
        self.T += dT
        
        self.T = np.clip(self.T, TEMP_MIN, TEMP_MAX)
        
        self.S = self._calculate_entropy()
    
    def get_color(self):
        """Get color based on temperature (blue=cold, red=hot)"""
        temp_ratio = (self.T - TEMP_MIN) / (TEMP_MAX - TEMP_MIN)
        temp_ratio = np.clip(temp_ratio, 0, 1)
        
        r = int(50 + 200 * temp_ratio)
        g = int(50 + 100 * (1 - abs(temp_ratio - 0.5) * 2))
        b = int(220 - 170 * temp_ratio)
        
        return (r, g, b)
    
    def reset(self):
        """Reset to initial state"""
        self.T = self.initial_T
        self.S = self._calculate_entropy()
        self.initial_S = self.S
        self.Q_absorbed = 0.0
    
    def get_state(self):
        """Return current state for display"""
        return {
            'T': self.T,
            'S': self.S,
            'dS': self.S - self.initial_S,
            'Q': self.Q_absorbed
        }


class HeatTransferSystem:
    """Manages heat transfer between two thermal bodies"""
    
    def __init__(self, body1, body2, thermal_conductivity):
        self.body1 = body1
        self.body2 = body2
        self.k = thermal_conductivity  # Thermal conductivity / heat transfer coefficient
        
        self.heat_flow_rate = 0.0  # Current heat flow rate (J/s)
        self.total_entropy_generated = 0.0  # Total entropy generated
        
        self.flow_particles = []
        self.particle_spawn_timer = 0.0
        self.particle_spawn_interval = 0.3  # seconds
        
        self.initial_total_entropy = body1.S + body2.S
    
    def update(self, dt):
        """Update heat transfer between bodies"""
        T1 = self.body1.T
        T2 = self.body2.T
        dT = T1 - T2
        
        self.heat_flow_rate = self.k * dT
        
        dQ = self.heat_flow_rate * dt
        
        if abs(dQ) > 1e-6:  # Only if significant heat transfer
            self.body1.add_heat(-dQ)  # Body 1 loses heat
            self.body2.add_heat(dQ)   # Body 2 gains heat
            
            if T1 > 0 and T2 > 0:
                dS_universe = dQ * (1.0/T2 - 1.0/T1)
                self.total_entropy_generated += dS_universe
        
        self._update_flow_particles(dt, dT)
    
    def _update_flow_particles(self, dt, dT):
        """Update heat flow visualization particles"""
        if abs(dT) > 1.0:  # Only if temperature difference is significant
            self.particle_spawn_timer += dt
            
            if self.particle_spawn_timer >= self.particle_spawn_interval:
                self.particle_spawn_timer = 0.0
                self._spawn_flow_particle(dT)
        
        for particle in self.flow_particles:
            if particle.active:
                particle.progress += dt * 1.5  # Speed of particle movement
                
                if particle.progress >= 1.0:
                    particle.active = False
                else:
                    particle.x = particle.target_x * particle.progress + (1 - particle.progress) * (self.body1.x + self.body1.width)
                    particle.y = particle.target_y * particle.progress + (1 - particle.progress) * (self.body1.y + self.body1.height // 2)
        
        self.flow_particles = [p for p in self.flow_particles if p.active]
    
    def _spawn_flow_particle(self, dT):
        """Spawn a new heat flow particle"""
        if len(self.flow_particles) >= NUM_FLOW_PARTICLES:
            return
        
        if dT > 0:  # Heat flows from body1 to body2
            start_x = self.body1.x + self.body1.width
            start_y = self.body1.y + self.body1.height // 2 + np.random.randint(-20, 20)
            target_x = self.body2.x
            target_y = self.body2.y + self.body2.height // 2 + np.random.randint(-20, 20)
        else:  # Heat flows from body2 to body1
            start_x = self.body2.x
            start_y = self.body2.y + self.body2.height // 2 + np.random.randint(-20, 20)
            target_x = self.body1.x + self.body1.width
            target_y = self.body1.y + self.body1.height // 2 + np.random.randint(-20, 20)
        
        particle = HeatFlowParticle(start_x, start_y, target_x, target_y)
        self.flow_particles.append(particle)
    
    def get_total_entropy(self):
        """Get total entropy of the system"""
        return self.body1.S + self.body2.S
    
    def get_entropy_change(self):
        """Get change in total entropy from initial state"""
        return self.get_total_entropy() - self.initial_total_entropy
    
    def reset(self):
        """Reset the system"""
        self.body1.reset()
        self.body2.reset()
        self.heat_flow_rate = 0.0
        self.total_entropy_generated = 0.0
        self.flow_particles = []
        self.particle_spawn_timer = 0.0
        self.initial_total_entropy = self.body1.S + self.body2.S
