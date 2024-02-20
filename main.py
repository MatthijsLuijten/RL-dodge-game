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
for episode in range(episodes):
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

            # TODO:
            # get agent action; action = agent.get_action(state)
            reward, next_state, done = env.step(1)

        clock.tick(60)  # Limit frame rate to 60 FPS

pygame.quit()
sys.exit()
