import os
import sys
import unittest
import pygame

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.player = Player((100, 100), size=10)

    def tearDown(self) -> None:
        pygame.quit()

    def test_initialization(self):
        self.assertEqual(self.player.location, (100, 100))
        self.assertEqual(self.player.size, 10)
        self.assertEqual(self.player.color, (255, 255, 255))

    def test_reset(self):
        self.player.location = (200, 200)
        self.player.reset()
        self.assertEqual(self.player.location, (100, 100))

    def test_move(self):
        self.player.move(self.player.actions[3])  # Move right
        self.assertEqual(self.player.location, (101, 100))

    def test_render(self):
        # Test render method. We can't really check rendering output in tests, but we can check if it raises any errors.
        try:
            self.player.render(self.screen)
        except Exception as e:
            self.fail(f"render() raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
