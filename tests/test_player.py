import os
import sys
import unittest
import pygame
from src.player import Player

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestPlayer(unittest.TestCase):
    def setUp(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.player = Player((100, 100), size=10)

    def tearDown(self) -> None:
        pygame.quit()

    def test_initialization(self):
        """Test if initializing a player sets the default size, location and color"""
        self.assertEqual(self.player.location, (100, 100))
        self.assertEqual(self.player.size, 10)
        self.assertEqual(self.player.color, (255, 255, 255))

    def test_reset(self):
        """Test if reseting a player sets its location to default"""
        self.player.location = (200, 200)
        self.player.reset()
        self.assertEqual(self.player.location, (100, 100))

    def test_move(self):
        """Test if moving a player updates the location correctly"""
        self.player.move(self.player.actions[3])  # Move right
        self.assertEqual(self.player.location, (101, 100))

    def test_render(self):
        """Test if rendering a player does not return any errors (we can't really check rendering output in tests)"""
        try:
            self.player.render(self.screen)
        except Exception as e:
            self.fail(f"render() raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
