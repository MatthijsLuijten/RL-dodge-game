import sys
import pygame

from src.environment.environment import Environment

pygame.init()
screen_size = (800, 600)  # Width x Height
screen = pygame.display.set_mode(size=screen_size)
pygame.display.set_caption("RL dodge game")
env = Environment(screen=screen, render_on=True)

clock = pygame.time.Clock()

while True:
    env.render()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
    clock.tick(60)  # Limit frame rate to 60 FPS
