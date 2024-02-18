from typing import Tuple
from agent import Agent


class Player(Agent):
    def __init__(self, start_location: Tuple[int, int], size: int = 10) -> None:
        super().__init__(start_location, size)

    def reset(self):
        self.location = self.start_location
