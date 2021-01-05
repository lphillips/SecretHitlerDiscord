import unittest
from secret_hitler import game


class GameInitTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.game = game.Game(0, 0, 10, 0)

    def test_game_init(self):
        """Test deck composition of liberal and fascist policies"""
        liberal_count = sum(map(lambda c: c == 'L', self.game.deck))
        fascist_count = sum(map(lambda c: c == 'F', self.game.deck))
        assert(liberal_count == 6)
        assert(fascist_count == 11)


if __name__ == '__main__':
    unittest.main()
