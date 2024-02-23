import pygame
import random
import numpy as np
from pygame.surface import Surface
from typing import Tuple, List

from src.enemy import Enemy
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

        self.enemies: list[Enemy] = []

        self.reset()

    def reset(self) -> np.ndarray:
        """
        Resets the environment.

        Returns:
            np.ndarray: Initial state of the environment.
        """
        self.player.reset()

        self.enemies = []

        if self.render_on:
            self.render()

        return self.get_state()

    def render(self) -> None:
        """
        Renders the environment.
        """
        self.screen.fill((0, 0, 0))
        self.player.render(self.screen)

        for enemy in self.enemies:
            enemy.render(self.screen)
        pygame.display.flip()

    def get_state(self) -> np.ndarray:
        """
        Gets the current state of the environment. This state is a list of coordinates, first the player's coordinates followed by the enemy
        coordinates, e.g. [400, 300, 10, 10].

        Returns:
            np.ndarray: Current state of the environment.
        """
        # Initialize a list to store distances between player and enemies
        distances = []

        # Calculate distances between player and enemies
        for enemy in self.enemies:
            enemy_pos = np.array(enemy.location)
            player_pos = np.array(self.player.location)
            distance = np.linalg.norm(enemy_pos - player_pos)  # Euclidean distance
            distances.append((enemy, distance))

        # Sort the enemies based on their distances from the player
        sorted_enemies = sorted(distances, key=lambda x: x[1])

        # Take the locations of the closest enemies, up to 10 or all if less than 10
        closest_enemy_locations: List[int] = []
        for enemy, _ in sorted_enemies[:10]:
            closest_enemy_locations.extend(enemy.location)

        # Fill remaining slots with -1 if there are fewer than 10 enemies
        num_missing_enemies = 10 - len(sorted_enemies)
        closest_enemy_locations += [-1] * (2 * num_missing_enemies)

        # Combine player location with locations of the closest enemies
        state = np.array(
            [self.player.location[0], self.player.location[1]] + closest_enemy_locations
        )

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
            print("not possible")
            return reward, done

        # Check if the player collides with an enemy
        for enemy in self.enemies:
            if self.check_collision(self.player, enemy):
                reward = self.rewards["death"]
                done = True
                print("death")
                return reward, done

        return reward, done

    def check_collision(self, player: Player, enemy: Enemy) -> bool:
        """
        Checks if there is a collision between the player and an enemy.

        Args:
            player (Player): The player object.
            enemy (Enemy): The enemy object.

        Returns:
            bool: True if there is a collision, False otherwise.
        """
        player_x, player_y = player.location
        enemy_x, enemy_y = enemy.location
        player_radius = player.size
        enemy_radius = enemy.size

        # Calculate distance between player and enemy
        distance = ((player_x - enemy_x) ** 2 + (player_y - enemy_y) ** 2) ** 0.5

        # Collision occurs if the distance is less than the sum of their radii
        return distance < (player_radius + enemy_radius)

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
        # print("reward", reward)
        next_state = self.get_state()

        for enemy in self.enemies:
            enemy.move()

            # Check if the enemy is outside the screen and remove it only if it's moving away from the screen
            # This ensures that self.enemies is not getting infinitely large
            if self.is_moving_outside_the_screen(enemy):
                self.enemies.remove(enemy)

        if self.render_on:
            self.render()

        return reward, next_state, done

    def is_moving_outside_the_screen(self, enemy: Enemy) -> bool:
        """
        Checks if the enemy is moving outside the screen based on its direction.

        Args:
            enemy (Enemy): The enemy object.

        Returns:
            bool: True if the enemy is moving outside the screen, False otherwise.
        """
        screen_width, screen_height = self.screen.get_size()
        enemy_x, enemy_y = enemy.location
        enemy_dx, enemy_dy = enemy.direction

        if (
            enemy_dx > 0 and enemy_x - enemy.size >= screen_width
        ):  # Moving right and positioned to or beyond the right of the screen
            return True
        elif (
            enemy_dx < 0 and enemy_x + enemy.size <= 0
        ):  # Moving left and positioned to or beyond the left of the screen
            return True
        elif (
            enemy_dy > 0 and enemy_y - enemy.size >= screen_height
        ):  # Moving down and positioned to or below the bottom of the screen
            return True
        elif (
            enemy_dy < 0 and enemy_y + enemy.size <= 0
        ):  # Moving up and positioned to or above the top of the screen
            return True
        else:
            return False

    def spawn_enemy(self):
        """
        Spawns a new enemy in the environment with random size and position in the border.
        """
        size = random.randint(10, 50)

        self.width, self.height = self.screen.get_size()

        # Choose a random border position
        border_position = random.choice(["top", "bottom", "left", "right"])

        # Create enemy position tuple based on chosen border
        if border_position == "top":
            start_location = (random.randint(0, self.width), 0)
            direction = (0, 1)
        elif border_position == "bottom":
            start_location = (random.randint(0, self.width), self.height)
            direction = (0, -1)
        elif border_position == "left":
            start_location = (0, random.randint(0, self.height))
            direction = (1, 0)
        elif border_position == "right":
            start_location = (self.width, random.randint(0, self.height))
            direction = (-1, 0)

        self.enemies.append(
            Enemy(start_location=start_location, direction=direction, size=size)
        )
