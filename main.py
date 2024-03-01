import os
import sys
import pygame
import matplotlib.pyplot as plt

from src.environment import Environment
from src.experience import Experience

render_on = True
render_interval = 10
screen = (800, 600)
episodes = 5000
experience_memory = 10000
if not os.path.exists("experiment_results"):
    os.mkdir("experiment_results")

if render_on:
    pygame.init()
    screen = pygame.display.set_mode(size=screen)
    pygame.display.set_caption("RL dodge game")
    clock = pygame.time.Clock()

env = Environment(screen=screen)

experiences = []
losses = []
rewards = []
epsilons = []

for episode in range(episodes):
    episode_reward = 0
    if episode % render_interval == 0:
        render_episode = True
    else:
        render_episode = False
    print(episode)
    state = env.reset()
    done = False
    step = 0
    while not done:
        if render_episode and render_on:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    pygame.quit()
                    sys.exit()

            env.render()
            # Update spawn timer
            clock.tick(60)  # Limit frame rate to 60 FPS

        # Check if it's time to spawn an enemy
        if step % 30 == 0:
            env.spawn_enemy()

        action = env.player.get_action(state)
        reward, next_state, done = env.step(action)
        episode_reward += reward

        experiences.append(Experience(state, action, reward, next_state, done))

        if len(experiences) >= experience_memory:
            loss = env.player.learn(experiences)
            losses.append(loss)
            experiences = []

        state = next_state
        step += 1

    rewards.append(episode_reward)
    epsilons.append(env.player.epsilon)

    # Plot and save
    plt.figure(figsize=(12, 6))
    plt.subplot(3, 1, 1)
    plt.plot(losses)
    plt.title("Losses")
    plt.subplot(3, 1, 2)
    plt.plot(rewards)
    plt.title("Rewards")
    plt.subplot(3, 1, 3)
    plt.plot(epsilons)
    plt.title("Epsilons")
    plt.tight_layout()
    plt.savefig("experiment_results/episode_plot_fast.png")
    plt.close()

    if episode % 50 == 0:
        env.player.save_model(f"models/model_{episode}_fast.h5")


pygame.quit()
sys.exit()
