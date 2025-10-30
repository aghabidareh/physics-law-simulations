import numpy as np
from config import (SCREEN_WIDTH, PIPE_SEGMENTS, SEGMENT_WIDTH,
                    NARROW_HEIGHT, WIDE_HEIGHT, FLUID_DENSITY, GRAVITY,
                    PARTICLE_RADIUS, PIPE_Y)


class PipeSegment:
    def __init__(self, index):
        self.index = index
        self.x = index * SEGMENT_WIDTH
        self.width = SEGMENT_WIDTH

        if index == PIPE_SEGMENTS // 2:
            self.height = NARROW_HEIGHT
        else:
            ratio = abs(index - PIPE_SEGMENTS // 2) / (PIPE_SEGMENTS // 2)
            self.height = NARROW_HEIGHT + (WIDE_HEIGHT - NARROW_HEIGHT) * ratio

        self.area = self.height * 1.0
        self.y = PIPE_Y + (WIDE_HEIGHT - self.height) / 2

    def calculate_velocity(self, base_velocity):
        reference_area = WIDE_HEIGHT
        return base_velocity * (reference_area / self.area)

    def calculate_pressure(self, velocity, reference_pressure, reference_velocity):
        dynamic_pressure_change = 0.5 * FLUID_DENSITY * (reference_velocity**2 - velocity**2)
        return reference_pressure + dynamic_pressure_change

    def contains_point(self, x, y):
        return (self.x <= x < self.x + self.width and
                self.y <= y < self.y + self.height)


class FluidParticle:
    def __init__(self, x, y, segment_index):
        self.position = np.array([float(x), float(y)], dtype=np.float64)
        self.segment_index = segment_index
        self.radius = PARTICLE_RADIUS
        self.active = True

    def update(self, dt, segments):
        if not self.active:
            return

        current_segment = segments[self.segment_index]
        velocity = current_segment.calculate_velocity(base_velocity=100.0)

        self.position[0] += velocity * dt

        if self.position[0] >= SCREEN_WIDTH:
            self.active = False
            return

        new_segment_index = int(self.position[0] / SEGMENT_WIDTH)
        new_segment_index = min(new_segment_index, len(segments) - 1)

        if new_segment_index != self.segment_index:
            self.segment_index = new_segment_index
            new_segment = segments[self.segment_index]

            segment_center_y = new_segment.y + new_segment.height / 2
            current_offset = self.position[1] - (current_segment.y + current_segment.height / 2)

            scale = new_segment.height / current_segment.height
            new_offset = current_offset * scale

            self.position[1] = segment_center_y + new_offset

        segment = segments[self.segment_index]
        min_y = segment.y + self.radius
        max_y = segment.y + segment.height - self.radius
        self.position[1] = np.clip(self.position[1], min_y, max_y)


class FluidSystem:
    def __init__(self):
        self.segments = [PipeSegment(i) for i in range(PIPE_SEGMENTS)]
        self.particles = []
        self.spawn_timer = 0.0
        self.spawn_interval = 0.05
        self.base_velocity = 100.0
        self.reference_pressure = 101325.0

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_particles()
            self.spawn_timer = 0.0

        for particle in self.particles:
            particle.update(dt, self.segments)

        self.particles = [p for p in self.particles if p.active]

    def spawn_particles(self):
        first_segment = self.segments[0]
        spacing = first_segment.height / 4

        for i in range(3):
            y = first_segment.y + spacing * (i + 1)
            particle = FluidParticle(10, y, 0)
            self.particles.append(particle)

    def get_segment_at_position(self, x):
        index = int(x / SEGMENT_WIDTH)
        index = min(max(index, 0), len(self.segments) - 1)
        return self.segments[index]

    def increase_flow_rate(self):
        self.base_velocity = min(self.base_velocity + 10.0, 200.0)

    def decrease_flow_rate(self):
        self.base_velocity = max(self.base_velocity - 10.0, 30.0)

    def reset(self):
        self.particles.clear()
        self.spawn_timer = 0.0
        self.base_velocity = 100.0