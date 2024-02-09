import pygame
import numpy as np


class Environment:
    def __init__(self, screen, agent_size=10, render_on=False):
        self.screen = screen
        self.render_on = render_on
        self.agent_size = agent_size

        self.agent_location = (
            (self.screen.get_size()[0] / 2),
            (self.screen.get_size()[1] / 2),
        )

        self.rewards = {
            "alive": 1,
            "death": -100,
            "not possible": -5,
        }

        self.actions = {
            "up": 0,
            "down": 1,
            "left": 2,
            "right": 3,
        }

    def reset(self):
        self.agent_location = (
            (self.screen.get_size()[0] / 2),
            (self.screen.get_size()[1] / 2),
        )

        # TODO: reset enemies; self.enemy_generator.reset()

        if self.render_on:
            self.render()

        return self.get_state()

    def render(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.circle(
            self.screen, (255, 255, 255), self.agent_location, self.agent_size
        )
        # TODO: draw enemeis; self.enemies.render()?
        pygame.display.flip()

    def get_state(self):
        # TODO: Add the closest enemy state here
        # Something like enemy_location = self.enemies.get_closest_enemy(self.agent_location, ...)
        state = np.array([self.agent_location])

        # TODO: if enemy state is added:
        # state = np.array([self.agent_location, enemy_distance])
        return state

    def move_agent(self, action):
        moves = {
            self.actions["up"]: (0, -1),
            self.actions["down"]: (0, 1),
            self.actions["left"]: (-1, 0),
            self.actions["right"]: (1, 0),
        }

        previous_location = self.agent_location

        move = moves.get(action)
        new_location = (previous_location[0] + move[0], previous_location[1] + move[1])

        done = False
        reward = self.rewards["alive"]

        if self.is_valid_location(new_location):
            reward = self.rewards["not possible"]
            done = True

        # TODO: check if the agent collides with an enemy, loop over enemies?
        # for enemy in self.enemy_generator.enemies: if enemy collides with agent: done = True reward = reward = self.rewards["death"]

        self.agent_location = new_location

        return reward, done

    def is_valid_location(self, new_location):
        screen_width, screen_height = self.screen.get_size()
        agent_radius = self.agent_size / 2

        x_min = agent_radius
        x_max = screen_width - agent_radius
        y_min = agent_radius
        y_max = screen_height - agent_radius

        if x_min <= new_location[0] <= x_max and y_min <= new_location[1] <= y_max:
            return True
        else:
            return False

    def step(self, action):
        # Apply the action to the environment, record the observations
        reward, done = self.move_agent(action)
        print("reward", reward)
        next_state = self.get_state()

        # TODO: Update enemy positions
        # self.enemies.step()?

        if self.render_on:
            self.render()

        return reward, next_state, done
