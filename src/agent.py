from typing import Tuple


class Agent:
    def __init__(self, start_location: Tuple[int, int], size: int) -> None:
        self.start_location = start_location
        self.location = start_location
        self.size = size

    def reset(self):
        pass

    def render(self):
        pass

    def move(self):
        pass
