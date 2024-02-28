import os
import sys
import unittest
import pygame

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.enemy import Enemy


class TestEnemy(unittest.TestCase):
    def setUp(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.enemy = Enemy(start_location=(100, 100), direction=(1, 0), size=10)

    def tearDown(self) -> None:
        pygame.quit()

    def test_initialization(self):
        """Test if initializing a enemy sets the default size, direction, location and color"""
        self.assertEqual(self.enemy.location, (100, 100))
        self.assertEqual(self.enemy.size, 10)
        self.assertEqual(self.enemy.direction, (1, 0))
        self.assertEqual(self.enemy.color, (255, 0, 0))

    def test_move(self):
        """Test if moving a enemy updates the location correctly"""
        self.enemy.move()  # Move right
        self.assertEqual(self.enemy.location, (101, 100))

    def test_render(self):
        """Test if rendering a enemy does not return any errors (we can't really check rendering output in tests)"""
        try:
            self.enemy.render(self.screen)
        except Exception as e:
            self.fail(f"render() raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
