import sys
import pygame

from src.environment import Environment

pygame.init()
screen_size = (800, 600)
screen = pygame.display.set_mode(size=screen_size)
pygame.display.set_caption("RL dodge game")
clock = pygame.time.Clock()

env = Environment(screen=screen, render_on=True)

episodes = 5000
spawn_interval = 0.5  # seconds

for episode in range(episodes):
    spawn_timer = 0
    state = env.reset()
    done = False

    while not done:
        env.render()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()

        # Update spawn timer
        spawn_timer += clock.get_time() / 1000

        # Check if it's time to spawn an enemy
        if spawn_timer >= spawn_interval:
            env.spawn_enemy()
            spawn_timer = 0

        # TODO:
        # get agent action; action = env.player.get_action(state)
        reward, next_state, done = env.step(0)

        clock.tick(60)  # Limit frame rate to 60 FPS

pygame.quit()
sys.exit()
