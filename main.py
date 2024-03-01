import random
import sys
import pygame
import matplotlib.pyplot as plt

from src.environment import Environment
from src.experience import Experience

# pygame.init()
screen_size = (800, 600)
# screen = pygame.display.set_mode(size=screen_size)
# pygame.display.set_caption("RL dodge game")
# clock = pygame.time.Clock()

# env = Environment(screen=screen, render_on=False)
env = Environment(screen=screen_size, render_on=False)

episodes = 5000
spawn_interval = 0.5  # seconds

render_interval = 10  # Render interval every 50 episodes
render_on = False

batch_size = 512
experiences = []
losses = []
rewards = []
epsilons = []

for episode in range(episodes):
    episode_reward = 0
    # if episode % render_interval == 0:  # Toggle rendering every 50 episodes
    #     render_on = True
    # else:
    #     render_on = False
    print(episode)
    spawn_timer = 0
    state = env.reset()
    done = False

    while not done:
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT or (
        #         event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        #     ):
        #         pygame.quit()
        #         sys.exit()
        # if render_on:  # Check if rendering is enabled
        #     env.render()

        # Update spawn timer
        # spawn_timer += clock.get_time() / 1000

        # Check if it's time to spawn an enemy
        if random.randint(0, 100) > 95:
            # if spawn_timer >= spawn_interval:
            env.spawn_enemy()
            spawn_timer = 0

        # print(state)
        action = env.player.get_action(state)
        reward, next_state, done = env.step(action)
        episode_reward += reward

        experiences.append(Experience(state, action, reward, next_state, done))

        if len(experiences) >= batch_size:
            loss = env.player.learn(experiences)
            losses.append(loss)
            experiences = []

        state = next_state
        # clock.tick(60)  # Limit frame rate to 60 FPS

    # if render_on:  # Check if rendering is enabled
    #     env.player.use_optimal_strategy = False

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
    plt.savefig(f"experiment_results/episode_plot_fast.png")
    plt.close()

    if episode % 50 == 0:
        env.player.save_model(f"models/model_{episode}_fast.h5")


pygame.quit()
sys.exit()
