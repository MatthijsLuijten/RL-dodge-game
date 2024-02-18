import pygame
import numpy as np
from pygame.surface import Surface
from typing import Tuple


class Environment:
    def __init__(
        self, screen: Surface, agent_size: int = 10, render_on: bool = False
    ) -> None:
        """
        Initializes the environment.

        Args:
            screen (Surface): Pygame screen surface.
            agent_size (int, optional): Size of the agent. Defaults to 10.
            render_on (bool, optional): Whether to render the environment. Defaults to False.
        """
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

        self.reset()

    def reset(self) -> np.ndarray:
        """
        Resets the environment.

        Returns:
            np.ndarray: Initial state of the environment.
        """
        self.agent_location = (
            (self.screen.get_size()[0] / 2),
            (self.screen.get_size()[1] / 2),
        )

        # TODO: reset enemies; self.enemy_generator.reset()? Dunno if needed

        if self.render_on:
            self.render()

        return self.get_state()

    def render(self) -> None:
        """
        Renders the environment.
        """
        self.screen.fill((0, 0, 0))
        pygame.draw.circle(
            self.screen, (255, 255, 255), self.agent_location, self.agent_size
        )
        # TODO: draw enemeis; self.enemies.render()?
        pygame.display.flip()

    def get_state(self) -> np.ndarray:
        """
        Gets the current state of the environment. This state is a list of coordinates, first the agents coordinates followed by the enemy
        coordinates, e.g. [400, 300, 10, 10].

        Returns:
            np.ndarray: Current state of the environment.
        """
        # TODO: Add the closest enemy state here
        # Something like enemy_location = self.enemies.get_closest_enemy(self.agent_location, ...)
        state = np.array([self.agent_location[0], self.agent_location[1]])

        # TODO: if enemy state is added:
        # state = np.array([self.agent_location[0], self.agent_location[1], enemy_location[0], enemy_location[1]])
        return state

    def move_agent(self, action: int) -> Tuple[int, bool]:
        """
        Moves the agent based on the action taken.

        Args:
            action (int): Action to be taken.

        Returns:
            Tuple[int, bool]: Reward obtained and whether the episode is done.
        """
        moves = {
            self.actions["up"]: (0, -1),
            self.actions["down"]: (0, 1),
            self.actions["left"]: (-1, 0),
            self.actions["right"]: (1, 0),
        }

        previous_location = self.agent_location

        move = moves.get(action, (0, 0))
        new_location = (previous_location[0] + move[0], previous_location[1] + move[1])

        done = False
        reward = self.rewards["alive"]

        if not self.is_valid_location(new_location):
            reward = self.rewards["not possible"]
            done = True

        # TODO: check if the agent collides with an enemy, loop over enemies?
        # for enemy in self.enemy_generator.enemies: if enemy collides with agent: done = True reward = reward = self.rewards["death"]

        self.agent_location = new_location

        return reward, done

    def is_valid_location(self, new_location: Tuple[int, int]) -> bool:
        """
        Checks if the new location is valid.

        Args:
            new_location (Tuple[int, int]): New location to be checked.

        Returns:
            bool: True if the location is valid, False otherwise.
        """
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

    def step(self, action: int) -> Tuple[int, np.ndarray, bool]:
        """
        Apply the action to the environment, record the observations.

        Args:
            action (int): Action to be taken.

        Returns:
            Tuple[int, np.ndarray, bool]: Reward obtained, next state, and whether the episode is done.
        """
        reward, done = self.move_agent(action)
        print("reward", reward)
        next_state = self.get_state()

        # TODO: Update enemy positions
        # self.enemies.step()?

        if self.render_on:
            self.render()

        return reward, next_state, done
