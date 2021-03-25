import unittest
from unittest.mock import Mock, MagicMock, patch, create_autospec
from secret_hitler import game, images


class GameInitTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.game = game.Game(0, 0, 10, 0)

    def test_game_init(self):
        """Test deck composition of liberal and fascist policies"""
        liberal_count = sum(map(lambda c: c == 'L', self.game.deck))
        fascist_count = sum(map(lambda c: c == 'F', self.game.deck))
        self.assertEqual(6, liberal_count)
        self.assertEqual(11, fascist_count)


class GameVoteFivePlayersTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.game = game.Game(MagicMock(), 0, 0, 5, 0)
        self.game.state = game.GameState.ELECTION
        add_players(self.game, 5)
        self.game.president = self.game.players[0]
        self.game.nominated = self.game.players[1]
        self.game.president_id = 0
        self.game.prev_president = self.game.players[4]
        self.game.prev_president_id = "test_player_5"

    def test_vote_outside_election(self):
        self.game.state = game.GameState.GAME_STARTING
        vote_result = self.game.vote("test_player_1", "y")
        self.assertEqual(game.VoteResult.NO_ELECTION, vote_result)
        self.assertEqual(game.GameState.GAME_STARTING, self.game.state)

    def test_valid_vote(self):
        vote_result = self.game.vote("test_player_1", "y")
        self.assertEqual(game.VoteResult.VALID, vote_result)
        self.assertEqual(game.GameState.ELECTION, self.game.state)

    def test_invalid_vote_bad_player(self):
        vote_result = self.game.vote("invalid_player", "y")
        self.assertEqual(game.VoteResult.INVALID, vote_result)
        self.assertEqual(game.GameState.ELECTION, self.game.state)

    def test_invalid_vote_multiple_votes(self):
        self.game.vote("test_player_1", "y")
        vote_result = self.game.vote("test_player_1", "n")
        self.assertEqual(game.VoteResult.INVALID, vote_result)
        self.assertEqual(game.GameState.ELECTION, self.game.state)
        self.assertEqual("y", self.game.votes["test_player_1"])

    @patch("secret_hitler.images.PolicyHandImage", MagicMock(spec=images.PolicyHandImage))
    def test_last_vote_pass(self):
        self.game.vote("test_player_1", "y")
        self.game.vote("test_player_2", "y")
        self.game.vote("test_player_3", "y")
        self.game.vote("test_player_4", "n")
        vote_result = self.game.vote("test_player_5", "n")
        self.assertEqual(game.VoteResult.CHANCELLOR_ELECTED, vote_result)
        self.assertEqual(game.GameState.LEGISLATIVE_PRESIDENT, self.game.state)
        self.assertEqual(0, self.game.failed_votes)
        self.assertEqual("test_player_1", self.game.president.get_id())
        self.assertEqual("test_player_2", self.game.chancellor.get_id())

    def test_last_vote_fail(self):
        self.game.vote("test_player_1", "y")
        self.game.vote("test_player_2", "y")
        self.game.vote("test_player_3", "n")
        self.game.vote("test_player_4", "n")
        vote_result = self.game.vote("test_player_5", "n")
        self.assertEqual(game.VoteResult.CHANCELLOR_REJECTED, vote_result)
        self.assertEqual(game.GameState.NOMINATION, self.game.state)
        self.assertEqual(1, self.game.failed_votes)
        self.assertEqual("test_player_2", self.game.president.get_id())
        self.assertIsNone(self.game.chancellor)

    def test_last_vote_fail_three_times(self):
        # Fail one
        self.game.vote("test_player_1", "y")
        self.game.vote("test_player_2", "y")
        self.game.vote("test_player_3", "n")
        self.game.vote("test_player_4", "n")
        self.game.vote("test_player_5", "n")

        # Fail two
        self.game.nominated = self.game.players[2]
        self.game.state = game.GameState.ELECTION
        self.game.vote("test_player_1", "y")
        self.game.vote("test_player_2", "y")
        self.game.vote("test_player_3", "n")
        self.game.vote("test_player_4", "n")
        self.game.vote("test_player_5", "n")

        # Fail three
        self.game.nominated = self.game.players[4]
        self.game.state = game.GameState.ELECTION
        self.game.vote("test_player_1", "y")
        self.game.vote("test_player_2", "y")
        self.game.vote("test_player_3", "n")
        self.game.vote("test_player_4", "n")
        vote_result = self.game.vote("test_player_5", "n")
        self.assertEqual(game.VoteResult.GOVERNMENT_IN_CHAOS, vote_result)
        self.assertEqual(game.GameState.NOMINATION, self.game.state)
        self.assertEqual(0, self.game.failed_votes)
        policy_placed = (self.game.liberal_board == 1) ^ (self.game.fascist_board == 1)
        self.assertTrue(policy_placed)
        self.assertEqual("test_player_4", self.game.president.get_id())
        self.assertIsNone(self.game.chancellor)


def add_players(test_game, count):
    for i in range(1, count+1):
        player_id = "test_player_" + str(i)
        if i == 0:
            role = "Hitler"
        elif i == 1:
            role = "Fascist"
        else:
            role = "Liberal"
        mock_player = MagicMock(game.Player)
        mock_player.player_id = player_id
        mock_player.get_id.return_value = player_id
        mock_player.role = role
        test_game.players.append(mock_player)


if __name__ == '__main__':
    unittest.main()
