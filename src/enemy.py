from typing import Tuple
from src.agent import Agent


class Enemy(Agent):
    def __init__(
        self,
        start_location: Tuple[int, int],
        direction: Tuple[int, int],
        size: int = 10,
        color: Tuple[int, int, int] = (255, 0, 0),
    ) -> None:
        """Intitalizes an enemy with start location, size, and default color (red).

        Args:
            start_location (Tuple[int, int]): The initial location of the enemy.
            direction (Tuple[int, int]): The direction the enemy will move in.
            size (int, optional): The size of the enemy.
            color (Tuple[int, int, int], optional): The color of the enemy.
        """
        super().__init__(start_location, size, color)
        self.direction = direction
        self.location = start_location
        self.size = size

    def move(self):
        """Moves the enemy in the specified direction."""
        super().move(self.direction)
