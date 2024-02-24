import pygame
import numpy as np
from typing import List, Tuple
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential, load_model

from src.agent import Agent
from src.experience import Experience


class Player(Agent):
    def __init__(
        self,
        start_location: Tuple[int, int],
        size: int = 10,
        epsilon=1,
        epsilon_decay=0.998,
        epsilon_end=0.01,
        gamma=0.99,
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

        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_end = epsilon_end
        self.gamma = gamma
        self.model = self.build_model()

    def reset(self):
        """Reset the player to its initial state."""
        self.location = self.start_location

    def build_model(self):
        """Create a sequential model with 3 layers."""
        model = Sequential(
            [
                # Input layer expects a flattened grid, hence the input shape is grid_size squared
                Dense(128, activation="relu", input_shape=(22,)),
                Dense(128, activation="relu"),
                Dense(64, activation="relu"),
                Dense(32, activation="relu"),
                Dense(4, activation="linear"),
            ]
        )

        optimizer = Adam(learning_rate=0.0001)
        model.compile(optimizer=optimizer, loss="mse")

        return model

    def get_action(self, state):
        # rand() returns a random value between 0 and 1
        if np.random.rand() <= self.epsilon:
            # Exploration: random action
            action = np.random.randint(0, 2)
        else:
            # Add an extra dimension to the state to create a batch with one instance
            state = np.expand_dims(state, axis=0)

            # Use the model to predict the Q-values (action values) for the given state
            q_values = self.model.predict(state, verbose=0)
            # print('Q-values:', q_values)

            # Select and return the action with the highest Q-value
            action = np.argmax(
                q_values[0]
            )  # Take the action from the first (and only) entry
            # print('action:', action)

        # Decay the epsilon value to reduce the exploration over time
        if self.epsilon > self.epsilon_end:
            self.epsilon *= self.epsilon_decay

        return action

    def learn(self, experiences: List[Experience]):
        """Trains the model based on the experiences gathered.

        This method takes a batch of experiences and uses them to train the model to better predict
        the expected future rewards for each action in a given state.

        Args:
            experiences (List[Experience]): A list of Experience objects representing the agent's interactions
                                             with the environment, including states, actions, rewards, next states,
                                             and episode termination flags.

        """
        states = np.array([experience.state for experience in experiences])
        actions = np.array([experience.action for experience in experiences])
        rewards = np.array([experience.reward for experience in experiences])
        next_states = np.array([experience.next_state for experience in experiences])
        dones = np.array([experience.done for experience in experiences])

        # Predict the Q-values (action values) for the given state batch
        current_q_values = self.model.predict(states, verbose=0)

        # Predict the Q-values for the next_state batch
        next_q_values = self.model.predict(next_states, verbose=0)

        # Initialize the target Q-values as the current Q-values
        target_q_values = current_q_values.copy()

        # Calculate the expected reward for each experience
        for i in range(len(experiences)):
            if dones[i]:
                target_q_values[i, actions[i]] = rewards[i]
            else:
                target_q_values[i, actions[i]] = rewards[i] + self.gamma * np.max(
                    next_q_values[i]
                )

        # Train the model
        self.model.fit(states, target_q_values, epochs=1, verbose=1)
