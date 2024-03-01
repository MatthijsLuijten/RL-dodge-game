import numpy as np


class Experience:
    def __init__(
        self,
        state: np.ndarray,
        action: int,
        reward: int,
        next_state: np.ndarray,
        done: bool,
    ) -> None:
        """Initializes an Experience instance with state, action, reward, next_state, and a done flag.

        Args:
            state (np.ndarray): The current state of the environment at the time of the experience.
            action (int): The action taken in the current state.
            reward (int): The reward received after taking the action in the current state.
            next_state (np.ndarray): The resulting state of the environment after taking the action.
            done (bool): A boolean flag indicating whether the episode terminates after this experience.
        """
        self.state = state
        self.action = action
        self.reward = reward
        self.next_state = next_state
        self.done = done
