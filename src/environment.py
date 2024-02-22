import pygame
import numpy as np
from pygame.surface import Surface
from typing import Tuple

from src.player import Player


class Environment:
    def __init__(
        self, screen: Surface, player_size: int = 10, render_on: bool = False
    ) -> None:
        """
        Initializes the environment.

        Args:
            screen (Surface): Pygame screen surface.
            player_size (int, optional): Size of the player. Defaults to 10.
            render_on (bool, optional): Whether to render the environment. Defaults to False.
        """
        self.screen = screen
        self.render_on = render_on

        self.player = Player(
            (
                (self.screen.get_size()[0] / 2),
                (self.screen.get_size()[1] / 2),
            ),
            player_size,
        )

        self.rewards = {
            "alive": 1,
            "death": -100,
            "not possible": -5,
        }

        self.reset()

    def reset(self) -> np.ndarray:
        """
        Resets the environment.

        Returns:
            np.ndarray: Initial state of the environment.
        """
        self.player.reset()

        # TODO: reset enemies; self.enemy_generator.reset()? Dunno if needed

        if self.render_on:
            self.render()

        return self.get_state()

    def render(self) -> None:
        """
        Renders the environment.
        """
        self.screen.fill((0, 0, 0))
        self.player.render(self.screen)

        # TODO: draw enemeis; self.enemies.render()?
        pygame.display.flip()

    def get_state(self) -> np.ndarray:
        """
        Gets the current state of the environment. This state is a list of coordinates, first the players coordinates followed by the enemy
        coordinates, e.g. [400, 300, 10, 10].

        Returns:
            np.ndarray: Current state of the environment.
        """
        # TODO: Add the closest enemy state here
        # Something like enemy_location = self.enemies.get_closest_enemy(self.player_location, ...)
        state = np.array([self.player.location[0], self.player.location[1]])

        # TODO: if enemy state is added:
        # state = np.array([self.player_location[0], self.player_location[1], enemy_location[0], enemy_location[1]])
        return state

    def move_player(self, action: int) -> Tuple[int, bool]:
        """
        Moves the player based on the action taken and determines the reward

        Args:
            action (int): Action to be taken.

        Returns:
            Tuple[int, bool]: Reward obtained and whether the episode is done.
        """

        self.player.move(self.player.actions[action])

        done = False
        reward = self.rewards["alive"]

        if not self.is_valid_location(self.player.location):
            reward = self.rewards["not possible"]
            done = True

        # TODO: check if the player collides with an enemy, loop over enemies?
        # for enemy in self.enemy_generator.enemies: if enemy collides with player: done = True reward = reward = self.rewards["death"]

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
        player_radius = self.player.size / 2

        x_min = player_radius
        x_max = screen_width - player_radius
        y_min = player_radius
        y_max = screen_height - player_radius

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
        reward, done = self.move_player(action)
        print("reward", reward)
        next_state = self.get_state()

        # TODO: Update enemy positions
        # self.enemies.step()?

        if self.render_on:
            self.render()

        return reward, next_state, done
