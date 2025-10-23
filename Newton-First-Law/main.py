import asyncio
import platform
import pygame
import numpy as np

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Newton's First Law Simulation")
FPS = 60
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

ball_pos = np.array([WIDTH / 2, HEIGHT / 2], dtype=float)
ball_vel = np.array([0.0, 0.0])
ball_radius = 20
mass = 1.0
friction_coeff = 0.1
friction_on = False

def apply_friction():
    global ball_vel, friction_on
    if friction_on and np.linalg.norm(ball_vel) > 0:
        vel_magnitude = np.linalg.norm(ball_vel)
        friction_dir = -ball_vel / vel_magnitude
        friction_force = friction_coeff * mass * 9.81 * friction_dir
        acceleration = friction_force / mass
        ball_vel += acceleration / FPS
        if np.linalg.norm(ball_vel) < 0.1:
            ball_vel = np.array([0.0, 0.0])

def update_loop():
    global ball_pos, ball_vel, friction_on
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        elif event.type == pygame.KEYDOWN:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    friction_on = not friction_on
                elif event.key == pygame.K_r:
                    ball_pos = np.array([WIDTH / 2, HEIGHT / 2], dtype=float)
                    ball_vel = np.array([np.random.uniform(-5, 5), np.random.uniform(-5, 5)])
                elif event.key == pygame.K_s:
                    ball_vel = np.array([0.0, 0.0])

    ball_pos += ball_vel

    apply_friction()

    if ball_pos[0] - ball_radius < 0 or ball_pos[0] + ball_radius > WIDTH:
        ball_vel[0] = -ball_vel[0]
        ball_pos[0] = np.clip(ball_pos[0], ball_radius, WIDTH - ball_radius)
    if ball_pos[1] - ball_radius < 0 or ball_pos[1] + ball_radius > HEIGHT:
        ball_vel[1] = -ball_vel[1]
        ball_pos[1] = np.clip(ball_pos[1], ball_radius, HEIGHT - ball_radius)

    screen.fill(WHITE)
    pygame.draw.circle(screen, RED if friction_on else BLUE, ball_pos, ball_radius)
    font = pygame.font.SysFont(None, 30)
    text = font.render("Press SPACE to toggle friction, R to reset with random velocity, S to stop", True, (0, 0, 0))
    screen.blit(text, (10, 10))
    status = font.render(f"Friction: {'ON' if friction_on else 'OFF'}", True, (0, 0, 0))
    screen.blit(status, (10, 40))
    pygame.display.flip()

def setup():
    pass

async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())