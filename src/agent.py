from typing import Tuple
import pygame


class Agent:
    def __init__(
        self, start_location: Tuple[int, int], size: int, color: Tuple[int, int, int]
    ) -> None:
        """Intializes an agent in the game.

        Args:
            start_location (Tuple[int, int]): The initial location of the agent.
            size (int): The size of the agent (radius).
            color (Tuple[int, int, int]): The color of the agent.
        """
        self.start_location = start_location
        self.location = start_location
        self.size = size
        self.color = color

    def reset(self) -> None:
        """Reset the agent to its initial state."""
        pass

    def render(self, screen: pygame.Surface) -> pygame.Rect:
        """Render the agent as a circle on the screen.

        Args:
            screen (pygame.Surface): The surface to render the agent on.

        Returns:
            pygame.Rect: the created circle.
        """
        return pygame.draw.circle(screen, self.color, self.location, self.size)

    def move(self, move: Tuple[int, int]) -> None:
        """Move the agent given a direction

        Args:
            move (Tuple[int, int]): The amount to move the agent in (x, y) direction.

        """
        self.location = (self.location[0] + move[0], self.location[1] + move[1])
