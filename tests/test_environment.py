import os
import sys
import unittest
import pygame
from pygame.surface import Surface
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.environment import Environment


class TestEnvironment(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = Surface((800, 600))
        self.env = Environment(self.screen, player_size=10)

    def tearDown(self):
        pygame.quit()

    def test_reset(self):
        """Test if resetting the enivornment sets the default environment"""
        initial_state = self.env.reset()
        self.assertTrue(np.array_equal(initial_state, np.array([400, 300])))

    def test_move_player(self):
        """Test if moving a player updates the location correctly and returns the correct reward and done flag"""
        self.env.reset()
        reward, done = self.env.move_player(3)  # Move right
        self.assertEqual(reward, 1)
        self.assertFalse(done)
        self.assertEqual(self.env.player.location, (401, 300))

    def test_is_valid_location(self):
        """Test if valid and invalid player locations are correctly identified"""
        valid_location = self.env.is_valid_location((400, 300))
        self.assertTrue(valid_location)
        invalid_location = self.env.is_valid_location((-100, -100))
        self.assertFalse(invalid_location)
        invalid_location_edge = self.env.is_valid_location((800, 100))
        self.assertFalse(invalid_location_edge)

    def test_step(self):
        """Test if performing a step correctly updates the state, reward and done flag"""
        self.env.reset()
        reward, next_state, done = self.env.step(0)  # Move up
        self.assertTrue(np.array_equal(next_state, np.array([400, 299])))
        self.assertEqual(reward, 1)
        self.assertEqual(done, False)


if __name__ == "__main__":
    unittest.main()
