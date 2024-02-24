import sys
import pygame

from src.environment import Environment
from src.experience import Experience

pygame.init()
screen_size = (800, 600)
screen = pygame.display.set_mode(size=screen_size)
pygame.display.set_caption("RL dodge game")
clock = pygame.time.Clock()

env = Environment(screen=screen, render_on=False)

episodes = 5000
spawn_interval = 0.5  # seconds

render_interval = 10  # Render interval every 50 episodes
render_on = False

batch_size = 512
experiences = []

for episode in range(episodes):
    if episode % render_interval == 0:  # Toggle rendering every 50 episodes
        render_on = True
    else:
        render_on = False
    print(episode)
    spawn_timer = 0
    state = env.reset()
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()
        if render_on:  # Check if rendering is enabled
            env.render()

        # Update spawn timer
        spawn_timer += clock.get_time() / 1000

        # Check if it's time to spawn an enemy
        if spawn_timer >= spawn_interval:
            env.spawn_enemy()
            spawn_timer = 0

        action = env.player.get_action(state)
        reward, next_state, done = env.step(action)

        experiences.append(Experience(state, action, reward, next_state, done))

        if len(experiences) >= batch_size:
            env.player.learn(experiences)
            experiences = []

        state = next_state
        clock.tick(60)  # Limit frame rate to 60 FPS

pygame.quit()
sys.exit()
