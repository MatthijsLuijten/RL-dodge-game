import pygame
import numpy as np

class Environment:
    def __init__(self, screen, agent_size=10, render_on=False):
        self.screen = screen
        self.render_on = render_on
        self.agent_size = agent_size

        self.agent_location = ((self.screen.get_size()[0] / 2) - (self.agent_size / 2), (self.screen.get_size()[1] / 2) - (self.agent_size / 2))

        self.rewards = {
            "alive": 1,
            "death": -100,
            "not possible": -5,
            # "star": 50,
        }

        self.actions = {
            "up": 0,
            "down": 1,
            "left": 2,
            "right": 3,
            # "upleft": 4,
            # "downleft": 5,
            # "upright": 6,
            # "downright": 7,
        }

    def reset(self):
        self.agent_location = ((self.screen.get_size()[0] / 2) - (self.agent_size / 2), (self.screen.get_size()[1] / 2) - (self.agent_size / 2))

        if self.render_on:
            self.render()

    def render(self):
        # Make black screen with white agent and update the screen
        self.screen.fill((0, 0, 0))
        pygame.draw.circle(self.screen, (255, 255, 255), self.agent_location, self.agent_size)
        pygame.display.flip()

    def get_state(self):
        # TODO: Add the enemy state here
        # Something like enemy_distance, enemy_location = self.enemy.get_closest_enemy(self.agent_location, ...)
        state = np.array([self.agent_location])
        return state

    def move_agent(self, action):
        # Define the changes in position based on the action
        moves = {
            self.actions["up"]: (0, -1),
            self.actions["down"]: (0, 1),
            self.actions["left"]: (-1, 0),
            self.actions["right"]: (1, 0)
        }

        previous_location = self.agent_location

        # Check if the action is valid and update the agent's position
        move = moves.get(action)
        new_location = (previous_location[0] + move[0], previous_location[1] + move[1])

        # Initialize reward
        reward = self.rewards["alive"]

        # Check for a valid move
        if self.is_valid_location(new_location):
            # Update agent's location
            self.agent_location = new_location
        else:
            reward = self.rewards["not possible"]

        return reward

    def is_valid_location(self, new_location):
        # Check if the agent is within the bounds of the screen
        screen_width, screen_height = self.screen.get_size()
        agent_radius = self.agent_size / 2

        # Calculate the boundaries considering the circular shape of the agent
        x_min = agent_radius
        x_max = screen_width - agent_radius
        y_min = agent_radius
        y_max = screen_height - agent_radius

        # Check if the new location is within the bounds
        if x_min <= new_location[0] <= x_max and y_min <= new_location[1] <= y_max:
            return True
        else:
            return False

    def step(self, action):
        # Apply the action to the environment, record the observations
        reward, done = self.move_agent(action)
        print('reward', reward)
        next_state = self.get_state()

        # TODO:
        # Update enemy positions
        # self.enemies.step()?

        # Render the grid at each step
        if self.render_on:
            self.render()

        return reward, next_state, done
