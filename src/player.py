from typing import Tuple
import pygame

from src.agent import Agent


class Player(Agent):
    def __init__(
        self,
        start_location: Tuple[int, int],
        size: int = 10,
    ) -> None:
        """Intitalizes the Player with start location, size, and default color (white).

        Args:
            start_location (Tuple[int, int]): The initial location of the player.
            size (int, optional): The size of the player (radius). Defaults to 10 pixels.
        """
        super().__init__(start_location, size, (255, 255, 255))

        self.actions = {
            0: (0, -1),  # Up
            1: (0, 1),  # Down
            2: (-1, 0),  # Left
            3: (1, 0),  # Right
        }

    def reset(self):
        """Reset the player to its initial state."""
        self.location = self.start_location
