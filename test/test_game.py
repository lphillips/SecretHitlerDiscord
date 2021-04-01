import unittest
from unittest.mock import Mock, MagicMock, patch, call
from secret_hitler import game, images


class GameInitTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.game = game.Game(MagicMock(), 0, 0, 10, 0)

    def test_game_init(self):
        """Test deck composition of liberal and fascist policies"""
        liberal_count = sum(map(lambda c: c == "L", self.game.deck))
        fascist_count = sum(map(lambda c: c == "F", self.game.deck))
        self.assertEqual(6, liberal_count)
        self.assertEqual(11, fascist_count)


class GameStartTestCase(unittest.TestCase):

    @patch("random.shuffle")
    def test_game_start(self, mock_shuffle):
        self.game = game.Game(MagicMock(), 0, 0, 5, 0)
        add_players(self.game, 5)
        mock_shuffle.reset_mock()

        # Note: This test asserts players are shuffled before roles.
        # This isn"t actually a requirement of game_start, just a
        # side-effect of how the test is written
        self.game.start_game()
        roles = ["Liberal", "Liberal", "Liberal", "Fascist", "Hitler"]
        shuffle_calls = [call.attribute.method(self.game.play_order), call.attribute.method(roles)]
        self.assertEqual(mock_shuffle.mock_calls, shuffle_calls)
        player_roles = map(lambda p: p.role, self.game.players.values())
        self.assertTrue(None not in player_roles)

    @patch("random.shuffle", MagicMock())
    def test_game_start_five_players(self):
        self.game = game.Game(MagicMock(), 0, 0, 5, 0)
        add_players(self.game, 5)

        self.game.start_game()
        self.assertEqual("Liberal", self.game.players["test_player_1"].role)
        self.assertEqual("Liberal", self.game.players["test_player_2"].role)
        self.assertEqual("Liberal", self.game.players["test_player_3"].role)
        self.assertEqual("Fascist", self.game.players["test_player_4"].role)
        self.assertEqual("Hitler", self.game.players["test_player_5"].role)

    @patch("random.shuffle", MagicMock())
    def test_game_start_six_players(self):
        self.game = game.Game(MagicMock(), 0, 0, 6, 0)
        add_players(self.game, 6)

        self.game.start_game()
        self.assertEqual("Liberal", self.game.players["test_player_1"].role)
        self.assertEqual("Liberal", self.game.players["test_player_2"].role)
        self.assertEqual("Liberal", self.game.players["test_player_3"].role)
        self.assertEqual("Liberal", self.game.players["test_player_4"].role)
        self.assertEqual("Fascist", self.game.players["test_player_5"].role)
        self.assertEqual("Hitler", self.game.players["test_player_6"].role)

    @patch("random.shuffle", MagicMock())
    def test_game_start_seven_players(self):
        self.game = game.Game(MagicMock(), 0, 0, 7, 0)
        add_players(self.game, 7)

        self.game.start_game()
        self.assertEqual("Liberal", self.game.players["test_player_1"].role)
        self.assertEqual("Liberal", self.game.players["test_player_2"].role)
        self.assertEqual("Liberal", self.game.players["test_player_3"].role)
        self.assertEqual("Liberal", self.game.players["test_player_4"].role)
        self.assertEqual("Fascist", self.game.players["test_player_5"].role)
        self.assertEqual("Fascist", self.game.players["test_player_6"].role)
        self.assertEqual("Hitler", self.game.players["test_player_7"].role)

    @patch("random.shuffle", MagicMock())
    def test_game_start_eight_players(self):
        self.game = game.Game(MagicMock(), 0, 0, 8, 0)
        add_players(self.game, 8)

        self.game.start_game()
        self.assertEqual("Liberal", self.game.players["test_player_1"].role)
        self.assertEqual("Liberal", self.game.players["test_player_2"].role)
        self.assertEqual("Liberal", self.game.players["test_player_3"].role)
        self.assertEqual("Liberal", self.game.players["test_player_4"].role)
        self.assertEqual("Liberal", self.game.players["test_player_5"].role)
        self.assertEqual("Fascist", self.game.players["test_player_6"].role)
        self.assertEqual("Fascist", self.game.players["test_player_7"].role)
        self.assertEqual("Hitler", self.game.players["test_player_8"].role)

    @patch("random.shuffle", MagicMock())
    def test_game_start_nine_players(self):
        self.game = game.Game(MagicMock(), 0, 0, 9, 0)
        add_players(self.game, 9)

        self.game.start_game()
        self.assertEqual("Liberal", self.game.players["test_player_1"].role)
        self.assertEqual("Liberal", self.game.players["test_player_2"].role)
        self.assertEqual("Liberal", self.game.players["test_player_3"].role)
        self.assertEqual("Liberal", self.game.players["test_player_4"].role)
        self.assertEqual("Liberal", self.game.players["test_player_5"].role)
        self.assertEqual("Fascist", self.game.players["test_player_6"].role)
        self.assertEqual("Fascist", self.game.players["test_player_7"].role)
        self.assertEqual("Fascist", self.game.players["test_player_8"].role)
        self.assertEqual("Hitler", self.game.players["test_player_9"].role)

    @patch("random.shuffle", MagicMock())
    def test_game_start_ten_players(self):
        self.game = game.Game(MagicMock(), 0, 0, 10, 0)
        add_players(self.game, 10)

        self.game.start_game()
        self.assertEqual("Liberal", self.game.players["test_player_1"].role)
        self.assertEqual("Liberal", self.game.players["test_player_2"].role)
        self.assertEqual("Liberal", self.game.players["test_player_3"].role)
        self.assertEqual("Liberal", self.game.players["test_player_4"].role)
        self.assertEqual("Liberal", self.game.players["test_player_5"].role)
        self.assertEqual("Liberal", self.game.players["test_player_6"].role)
        self.assertEqual("Fascist", self.game.players["test_player_7"].role)
        self.assertEqual("Fascist", self.game.players["test_player_8"].role)
        self.assertEqual("Fascist", self.game.players["test_player_9"].role)
        self.assertEqual("Hitler", self.game.players["test_player_10"].role)


class GameNominateTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.game = game.Game(MagicMock(), 0, 0, 5, 0)
        add_players(self.game, 5)
        self.game._president_ = self.game.players["test_player_1"]
        self.game.state = game.GameState.NOMINATION

    def test_nominate_eligible(self):
        result = self.game.nominate("test_player_2")
        self.assertTrue(result)
        self.assertEqual(game.GameState.ELECTION, self.game.state)

    def test_nominate_self(self):
        result = self.game.nominate("test_player_1")
        self.assertFalse(result)
        self.assertEqual(game.GameState.NOMINATION, self.game.state)

    def test_nominate_prev_chancellor(self):
        # The "previous chancellor" is still set as the current
        # chancellor during nomination. A successful election is
        # what unseats a chancellor.
        self.game.chancellor = self.game.players["test_player_2"]
        self.game.chancellor_id = "test_player_2"
        result = self.game.nominate("test_player_2")
        self.assertFalse(result)
        self.assertEqual(game.GameState.NOMINATION, self.game.state)

    def test_nominate_prev_president_five_players(self):
        self.game.prev_president = self.game.players["test_player_2"]
        result = self.game.nominate("test_player_2")
        self.assertTrue(result)
        self.assertEqual(game.GameState.ELECTION, self.game.state)

    def test_nominate_prev_president_six_players(self):
        # Override the default set up
        self.game = game.Game(MagicMock(), 0, 0, 6, 0)
        add_players(self.game, 6)
        self.game._president_ = self.game.players["test_player_1"]
        self.game.state = game.GameState.NOMINATION

        self.game.prev_president = self.game.players["test_player_2"]
        result = self.game.nominate("test_player_2")
        self.assertFalse(result)
        self.assertEqual(game.GameState.NOMINATION, self.game.state)


class GameVoteTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.game = game.Game(MagicMock(), 0, 0, 5, 0)
        self.game.state = game.GameState.ELECTION
        add_players(self.game, 5)
        self.game._president_ = self.game.players["test_player_1"]
        self.game.nominated = self.game.players["test_player_2"]
        self.game.prev_president = self.game.players["test_player_5"]

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

    @patch("secret_hitler.images.PolicyHandImage")
    def test_election_pass(self, image_mock):
        self.game.deck = ["F", "F", "L", "L", "L", "L", "L", "L", "F", "F", "F", "F", "F", "F", "F", "F", "F"]
        self.game.vote("test_player_1", "y")
        self.game.vote("test_player_2", "y")
        self.game.vote("test_player_3", "y")
        self.game.vote("test_player_4", "n")
        vote_result = self.game.vote("test_player_5", "n")
        self.assertEqual(game.VoteResult.CHANCELLOR_ELECTED, vote_result)
        self.assertEqual(game.GameState.LEGISLATIVE_PRESIDENT, self.game.state)
        self.assertEqual(0, self.game.failed_votes)
        self.assertEqual("test_player_1", self.game.current_president.get_id())
        self.assertEqual("test_player_2", self.game.chancellor.get_id())
        image_mock.assert_called_once_with(["F", "F", "L"])

    def test_elect_hitler(self):
        self.game._president_ = self.game.players["test_player_4"]
        self.game.nominated = self.game.players["test_player_1"]
        self.game.fascist_board = 3

        self.game.vote("test_player_1", "y")
        self.game.vote("test_player_2", "y")
        self.game.vote("test_player_3", "y")
        self.game.vote("test_player_4", "n")
        vote_result = self.game.vote("test_player_5", "n")
        self.assertEqual(game.VoteResult.CHANCELLOR_ELECTED, vote_result)
        self.assertEqual(game.GameState.GAME_OVER, self.game.state)

    def test_election_fail(self):
        self.game.vote("test_player_1", "y")
        self.game.vote("test_player_2", "y")
        self.game.vote("test_player_3", "n")
        self.game.vote("test_player_4", "n")
        vote_result = self.game.vote("test_player_5", "n")
        self.assertEqual(game.VoteResult.CHANCELLOR_REJECTED, vote_result)
        self.assertEqual(game.GameState.NOMINATION, self.game.state)
        self.assertEqual(1, self.game.failed_votes)
        self.assertEqual("test_player_2", self.game.current_president.get_id())
        self.assertIsNone(self.game.chancellor)

    def test_election_fail_three_times(self):
        # Fail one
        self.game.vote("test_player_1", "y")
        self.game.vote("test_player_2", "y")
        self.game.vote("test_player_3", "n")
        self.game.vote("test_player_4", "n")
        self.game.vote("test_player_5", "n")

        # Fail two
        self.game.nominated = self.game.players["test_player_3"]
        self.game.state = game.GameState.ELECTION
        self.game.vote("test_player_1", "y")
        self.game.vote("test_player_2", "y")
        self.game.vote("test_player_3", "n")
        self.game.vote("test_player_4", "n")
        self.game.vote("test_player_5", "n")

        # Fail three
        self.game.nominated = self.game.players["test_player_5"]
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
        self.assertEqual("test_player_4", self.game.current_president.get_id())
        self.assertIsNone(self.game.chancellor)


class GameTestPresidentDiscardPolicy(unittest.TestCase):
    def setUp(self) -> None:
        self.game = game.Game(MagicMock(), 0, 0, 5, 0)
        add_players(self.game, 5)
        self.game.policies = ["F", "F", "L"]
        self.game.state = game.GameState.LEGISLATIVE_PRESIDENT
        self.game._president_ = self.game.players["test_player_1"]
        self.game.chancellor = self.game.players["test_player_2"]
        self.game.prev_president = self.game.players["test_player_5"]

    @patch("secret_hitler.images.PolicyHandImage")
    def test_valid_discard(self, image_mock):
        success = self.game.discard_policy("test_player_1", "F")
        self.assertTrue(success)
        self.assertEqual(game.GameState.LEGISLATIVE_CHANCELLOR, self.game.state)
        self.assertListEqual(["F", "L"], self.game.policies)
        self.assertListEqual(["F"], self.game.discard)
        image_mock.assert_called_once_with(["F", "L"])

    def test_invalid_discard(self):
        self.game.policies = ["L", "L", "L"]
        success = self.game.discard_policy("test_player_1", "F")
        self.assertFalse(success)
        self.assertEqual(game.GameState.LEGISLATIVE_PRESIDENT, self.game.state)
        self.assertListEqual(["L", "L", "L"], self.game.policies)
        self.assertListEqual([], self.game.discard)


class GameTestChancellorDiscardPolicy(unittest.TestCase):
    def setUp(self) -> None:
        self.game = game.Game(MagicMock(), 0, 0, 5, 0)
        add_players(self.game, 5)
        self.game.policies = ["F", "L"]
        self.game.state = game.GameState.LEGISLATIVE_CHANCELLOR
        self.game._president_ = self.game.players["test_player_1"]
        self.game.chancellor = self.game.players["test_player_2"]
        self.game.prev_president = self.game.players["test_player_5"]

    def test_place_liberal_policy(self):
        self.game.policies = ["L", "L"]
        success = self.game.discard_policy("test_player_2", "L")
        self.assertTrue(success)
        self.assertEqual(game.GameState.NOMINATION, self.game.state)
        self.assertEqual("test_player_2", self.game.current_president.get_id())
        self.assertListEqual([], self.game.policies)
        self.assertListEqual(["L"], self.game.discard)

    def test_place_fascist_policy(self):
        self.game.policies = ["F", "F"]
        success = self.game.discard_policy("test_player_2", "F")
        self.assertTrue(success)
        self.assertEqual(game.GameState.NOMINATION, self.game.state)
        self.assertEqual("test_player_2", self.game.current_president.get_id())
        self.assertListEqual([], self.game.policies)
        self.assertListEqual(["F"], self.game.discard)

    def test_invalid_discard(self):
        self.game.policies = ["F", "F"]
        success = self.game.discard_policy("test_player_2", "L")
        self.assertFalse(success)
        self.assertEqual(game.GameState.LEGISLATIVE_CHANCELLOR, self.game.state)
        self.assertEqual("test_player_1", self.game.current_president.get_id())
        self.assertListEqual(["F", "F"], self.game.policies)
        self.assertListEqual([], self.game.discard)


class GameTestExecute(unittest.TestCase):
    def setUp(self) -> None:
        self.game = game.Game(MagicMock(), 0, 0, 5, 0)
        add_players(self.game, 5)
        self.game.state = game.GameState.EXECUTION
        self.game._president_ = self.game.players["test_player_1"]
        self.game.chancellor = self.game.players["test_player_2"]
        self.game.prev_president = self.game.players["test_player_5"]

    def test_valid_execute(self):
        expected_executed_player = self.game.players["test_player_5"]
        executed_player = self.game.execute_player("test_player_5")
        self.assertEqual(expected_executed_player, executed_player)
        self.assertEqual(game.GameState.NOMINATION, self.game.state)
        self.assertEqual("test_player_2", self.game.current_president.get_id())
        self.assertIsNone(self.game.players.get("test_player_5"))
        self.assertFalse(expected_executed_player in self.game.play_order)

    def test_invalid_execute(self):
        executed_player = self.game.execute_player("bogus_player")
        expected_players = self.game.players
        expected_play_order = self.game.play_order
        self.assertIsNone(executed_player)
        self.assertEqual(game.GameState.EXECUTION, self.game.state)
        self.assertEqual("test_player_1", self.game.current_president.get_id())
        self.assertEqual(expected_players, self.game.players)
        self.assertEqual(expected_play_order, self.game.play_order)

    def test_execute_hitler(self):
        expected_executed_player = self.game.players["test_player_1"]
        executed_player = self.game.execute_player("test_player_1")
        self.assertEqual(expected_executed_player, executed_player)
        self.assertEqual(game.GameState.GAME_OVER, self.game.state)
        self.assertIsNone(self.game.players.get("test_player_1"))
        self.assertFalse(expected_executed_player in self.game.play_order)


class GameTestPolicyPeek(unittest.TestCase):
    def setUp(self) -> None:
        self.game = game.Game(MagicMock(), 0, 0, 5, 0)
        add_players(self.game, 5)
        self.game.state = game.GameState.LEGISLATIVE_CHANCELLOR
        self.game.fascist_board = 2
        self.game._president_ = self.game.players["test_player_1"]
        self.game.chancellor = self.game.players["test_player_2"]
        self.game.prev_president = self.game.players["test_player_5"]

    @patch("secret_hitler.images.PolicyHandImage")
    def test_policy_peek(self, image_mock):
        self.game.policies = ["F", "F"]
        self.game.deck = ["F", "L", "F", "L"]
        self.game.discard_policy("test_player_2", "F")
        self.assertEqual(game.GameState.POLICY_PEEK, self.game.state)
        self.assertTrue(self.game.peeked)
        image_mock.assert_called_once_with(["F", "L", "F"])

        self.game.finish_policy_peek()
        self.assertEqual(game.GameState.NOMINATION, self.game.state)
        self.assertEqual("test_player_2", self.game.current_president.get_id())
        self.assertListEqual([], self.game.policies)


class GameTestInvestigation(unittest.TestCase):
    def setUp(self) -> None:
        self.game = game.Game(MagicMock(), 0, 0, 7, 0)
        add_players(self.game, 7)
        self.game.state = game.GameState.LEGISLATIVE_CHANCELLOR
        self.game.fascist_board = 1
        self.game._president_ = self.game.players["test_player_1"]
        self.game.chancellor = self.game.players["test_player_2"]
        self.game.prev_president = self.game.players["test_player_5"]

    def test_investigate_hitler(self):
        party = self.game.investigate_player("test_player_1")
        self.assertEqual("Fascist", party)
        self.assertEqual(game.GameState.NOMINATION, self.game.state)
        self.assertEqual("test_player_2", self.game.current_president.get_id())

    def test_investigate_fascist(self):
        party = self.game.investigate_player("test_player_2")
        self.assertEqual("Fascist", party)
        self.assertEqual(game.GameState.NOMINATION, self.game.state)
        self.assertEqual("test_player_2", self.game.current_president.get_id())

    def test_investigate_liberal(self):
        party = self.game.investigate_player("test_player_3")
        self.assertEqual("Liberal", party)
        self.assertEqual(game.GameState.NOMINATION, self.game.state)
        self.assertEqual("test_player_2", self.game.current_president.get_id())


class GameTestSpecialElection(unittest.TestCase):
    def setUp(self) -> None:
        self.game = game.Game(MagicMock(), 0, 0, 5, 0)
        add_players(self.game, 5)
        self.game.state = game.GameState.SPECIAL_ELECTION
        self.game.fascist_board = 3
        self.game._president_ = self.game.players["test_player_1"]
        self.game.chancellor = self.game.players["test_player_2"]
        self.game.prev_president = self.game.players["test_player_3"]

    def test_valid_special_election(self):
        self.game.special_election("test_player_3")
        self.assertEqual(game.GameState.NOMINATION, self.game.state)
        self.assertEqual("test_player_3", self.game.current_president.get_id())

        # Nominate a chancellor and fail the vote to see if the next
        # president is chosen correctly
        self.game.nominate("test_player_4")
        self.game.vote("test_player_1", "n")
        self.game.vote("test_player_2", "n")
        self.game.vote("test_player_3", "n")
        self.game.vote("test_player_4", "n")
        self.game.vote("test_player_5", "n")

        self.assertEqual(game.GameState.NOMINATION, self.game.state)
        self.assertEqual("test_player_2", self.game.current_president.get_id())
        self.assertEqual("test_player_3", self.game.prev_president.get_id())

    def test_special_election_current_president(self):
        self.game.special_election("test_player_1")
        self.assertEqual(game.GameState.SPECIAL_ELECTION, self.game.state)
        self.assertEqual("test_player_1", self.game.current_president.get_id())


class GameVetoTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.game = game.Game(MagicMock(), 0, 0, 5, 0)
        add_players(self.game, 5)
        self.game.state = game.GameState.LEGISLATIVE_CHANCELLOR
        self.game.fascist_board = 5
        self.game.deck = ["F"]
        self.game.policies = ["F", "F"]
        self.game._president_ = self.game.players["test_player_1"]
        self.game.chancellor = self.game.players["test_player_2"]
        self.game.prev_president = self.game.players["test_player_3"]

    def test_valid_veto_request(self):
        success = self.game.request_veto("test_player_2")
        self.assertTrue(success)
        self.assertEqual(game.GameState.VETO, self.game.state)

    def test_invalid_player_veto_request(self):
        success = self.game.request_veto("test_player_4")
        self.assertFalse(success)
        self.assertEqual(game.GameState.LEGISLATIVE_CHANCELLOR, self.game.state)
        self.assertEqual("test_player_1", self.game.current_president.get_id())
        self.assertListEqual([], self.game.discard)
        self.assertListEqual(["F", "F"], self.game.policies)

    def test_invalid_state_veto_request(self):
        self.game.state = game.GameState.NOMINATION
        success = self.game.request_veto("test_player_2")
        self.assertFalse(success)
        self.assertEqual(game.GameState.NOMINATION, self.game.state)
        self.assertEqual("test_player_1", self.game.current_president.get_id())
        self.assertListEqual([], self.game.discard)
        self.assertListEqual(["F", "F"], self.game.policies)

    def test_accepted_veto(self):
        self.game.state = game.GameState.VETO

        success = self.game.veto("test_player_1", True)
        self.assertTrue(success)
        self.assertEqual(game.GameState.NOMINATION, self.game.state)
        self.assertEqual(1, self.game.failed_votes)
        self.assertEqual("test_player_2", self.game.current_president.get_id())
        self.assertListEqual(["F", "F"], self.game.discard)
        self.assertListEqual([], self.game.policies)

    @patch("secret_hitler.images.PolicyHandImage", MagicMock(spec=images.PolicyHandImage))
    def test_rejected_veto(self):
        self.game.state = game.GameState.VETO

        success = self.game.veto("test_player_1", False)
        self.assertTrue(success)
        self.assertEqual(game.GameState.LEGISLATIVE_CHANCELLOR, self.game.state)
        self.assertEqual(0, self.game.failed_votes)
        self.assertEqual("test_player_1", self.game.current_president.get_id())
        self.assertListEqual([], self.game.discard)
        self.assertListEqual(["F", "F"], self.game.policies)

    def test_accepted_veto_government_in_chaos(self):
        self.game.failed_votes = 2
        self.game.state = game.GameState.VETO

        # The deck only has one fascist policy, so the result of these steps should be GAME_OVER
        success = self.game.veto("test_player_1", True)
        self.assertTrue(success)
        self.assertEqual(game.GameState.GAME_OVER, self.game.state)
        self.assertEqual(0, self.game.failed_votes)
        self.assertEqual("test_player_1", self.game.current_president.get_id())
        self.assertListEqual(["F", "F"], self.game.discard)
        self.assertListEqual([], self.game.policies)


class GameTestLiberalBoardStates(unittest.TestCase):
    def setUp(self) -> None:
        self.player_count = 5
        self.game = game.Game(MagicMock(), 0, 0, self.player_count, 0)
        self.game.add_player("test_player_1", "Player 1", "p1")
        self.game.add_player("test_player_2", "Player 2", "p2")
        self.game.add_player("test_player_3", "Player 3", "p3")
        self.game.add_player("test_player_4", "Player 4", "p4")
        self.game.add_player("test_player_5", "Player 5", "p5")
        self.game.deck = ["L", "L", "L", "L", "L", "L", "L", "L", "L", "L", "L", "L", "L", "L", "L", "L", "L"]
        # self.game._president_ = self.game.players["test_player_1"]

    @patch("secret_hitler.images.PolicyHandImage", MagicMock(spec=images.PolicyHandImage))
    @patch("random.shuffle", MagicMock())
    def test_liberal_board_flow(self):
        self.game.start_game()
        self.assertEqual("Liberal", self.game.players["test_player_1"].role)
        self.assertEqual("Liberal", self.game.players["test_player_2"].role)
        self.assertEqual("Liberal", self.game.players["test_player_3"].role)
        self.assertEqual("Fascist", self.game.players["test_player_4"].role)
        self.assertEqual("Hitler", self.game.players["test_player_5"].role)

        game_round(self.game, self.player_count, "test_player_1", "test_player_2", "L")
        self.assertEqual(game.GameState.NOMINATION, self.game.state)

        game_round(self.game, self.player_count, "test_player_2", "test_player_3", "L")
        self.assertEqual(game.GameState.NOMINATION, self.game.state)

        game_round(self.game, self.player_count, "test_player_3", "test_player_4", "L")
        self.assertEqual(game.GameState.NOMINATION, self.game.state)

        game_round(self.game, self.player_count, "test_player_4", "test_player_5", "L")
        self.assertEqual(game.GameState.NOMINATION, self.game.state)

        game_round(self.game, self.player_count, "test_player_5", "test_player_1", "L")
        self.assertEqual(game.GameState.GAME_OVER, self.game.state)
        self.assertEqual("Liberal", self.game.winner)


class GameTestFascistBoardOneStates(unittest.TestCase):
    def setUp(self) -> None:
        self.player_count = 5
        self.game = game.Game(MagicMock(), 0, 0, self.player_count, 0)
        add_players(self.game, self.player_count)
        self.game.deck = ["F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F"]
        # self.game._president_ = self.game.players["test_player_1"]

    @patch("secret_hitler.images.PolicyHandImage", MagicMock(spec=images.PolicyHandImage))
    @patch("random.shuffle", MagicMock())
    def test_fascist_board_one_flow(self):
        self.game.start_game()

        game_round(self.game, self.player_count, "test_player_1", "test_player_2", "F")
        self.assertEqual(game.GameState.NOMINATION, self.game.state)

        game_round(self.game, self.player_count, "test_player_2", "test_player_3", "F")
        self.assertEqual(game.GameState.NOMINATION, self.game.state)

        game_round(self.game, self.player_count, "test_player_3", "test_player_4", "F")
        self.assertEqual(game.GameState.POLICY_PEEK, self.game.state)
        self.game.finish_policy_peek()
        self.assertEqual(game.GameState.NOMINATION, self.game.state)

        game_round(self.game, self.player_count, "test_player_4", "test_player_1", "F")
        self.assertEqual(game.GameState.EXECUTION, self.game.state)
        self.game.execute_player("test_player_1")
        self.assertEqual(game.GameState.NOMINATION, self.game.state)

        game_round(self.game, self.player_count, "test_player_5", "test_player_2", "F")
        self.assertEqual(game.GameState.EXECUTION, self.game.state)
        self.game.execute_player("test_player_2")
        self.assertEqual(game.GameState.NOMINATION, self.game.state)

        game_round(self.game, self.player_count, "test_player_3", "test_player_4", "F")
        self.assertEqual(game.GameState.GAME_OVER, self.game.state)


class GameTestFascistBoardTwoStates(unittest.TestCase):
    def setUp(self) -> None:
        self.player_count = 7
        self.game = game.Game(MagicMock(), 0, 0, self.player_count, 0)
        add_players(self.game, self.player_count)
        self.game.deck = ["F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F"]

    @patch("secret_hitler.images.PolicyHandImage", MagicMock(spec=images.PolicyHandImage))
    @patch("random.shuffle", MagicMock())
    def test_fascist_board_two_flow(self):
        self.game.start_game()

        game_round(self.game, self.player_count, "test_player_1", "test_player_2", "F")
        self.assertEqual(game.GameState.NOMINATION, self.game.state)

        game_round(self.game, self.player_count, "test_player_2", "test_player_3", "F")
        self.assertEqual(game.GameState.INVESTIGATION, self.game.state)
        self.game.investigate_player("test_player_1")
        self.assertEqual(game.GameState.NOMINATION, self.game.state)

        game_round(self.game, self.player_count, "test_player_3", "test_player_4", "F")
        self.assertEqual(game.GameState.SPECIAL_ELECTION, self.game.state)
        self.game.special_election("test_player_6")
        self.assertEqual(game.GameState.NOMINATION, self.game.state)

        game_round(self.game, self.player_count, "test_player_6", "test_player_1", "F")
        self.assertEqual(game.GameState.EXECUTION, self.game.state)
        self.game.execute_player("test_player_1")
        self.assertEqual(game.GameState.NOMINATION, self.game.state)

        game_round(self.game, self.player_count, "test_player_4", "test_player_5", "F")
        self.assertEqual(game.GameState.EXECUTION, self.game.state)
        self.game.execute_player("test_player_2")
        self.assertEqual(game.GameState.NOMINATION, self.game.state)

        game_round(self.game, self.player_count, "test_player_5", "test_player_3", "F")
        self.assertEqual(game.GameState.GAME_OVER, self.game.state)


class GameTestFascistBoardThreeStates(unittest.TestCase):
    def setUp(self) -> None:
        self.player_count = 9
        self.game = game.Game(MagicMock(), 0, 0, self.player_count, 0)
        add_players(self.game, self.player_count)
        self.game.deck = ["F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F"]

    @patch("secret_hitler.images.PolicyHandImage", MagicMock(spec=images.PolicyHandImage))
    @patch("random.shuffle", MagicMock())
    def test_fascist_board_three_flow(self):
        self.game.start_game()

        game_round(self.game, self.player_count, "test_player_1", "test_player_2", "F")
        self.assertEqual(game.GameState.INVESTIGATION, self.game.state)
        self.game.investigate_player("test_player_1")
        self.assertEqual(game.GameState.NOMINATION, self.game.state)

        game_round(self.game, self.player_count, "test_player_2", "test_player_3", "F")
        self.assertEqual(game.GameState.INVESTIGATION, self.game.state)
        self.game.investigate_player("test_player_2")
        self.assertEqual(game.GameState.NOMINATION, self.game.state)

        game_round(self.game, self.player_count, "test_player_3", "test_player_4", "F")
        self.assertEqual(game.GameState.SPECIAL_ELECTION, self.game.state)
        self.game.special_election("test_player_9")
        self.assertEqual(game.GameState.NOMINATION, self.game.state)

        game_round(self.game, self.player_count, "test_player_9", "test_player_8", "F")
        self.assertEqual(game.GameState.EXECUTION, self.game.state)
        self.game.execute_player("test_player_1")
        self.assertEqual(game.GameState.NOMINATION, self.game.state)

        game_round(self.game, self.player_count, "test_player_4", "test_player_5", "F")
        self.assertEqual(game.GameState.EXECUTION, self.game.state)
        self.game.execute_player("test_player_2")
        self.assertEqual(game.GameState.NOMINATION, self.game.state)

        game_round(self.game, self.player_count, "test_player_5", "test_player_6", "F")
        self.assertEqual(game.GameState.GAME_OVER, self.game.state)


def add_players(test_game, count):
    for i in range(1, count+1):
        player_id = "test_player_" + str(i)
        if i == 1:
            role = "Hitler"
            party = "Fascist"
        elif i == 2:
            role = "Fascist"
            party = "Fascist"
        else:
            role = "Liberal"
            party = "Liberal"
        mock_player = MagicMock(game.Player)
        mock_player.player_id = player_id
        mock_player.get_id.return_value = player_id
        mock_player.role = role
        mock_player.party = party
        mock_player.get_party.return_value = party
        test_game.players[player_id] = mock_player
        test_game.play_order.append(mock_player)


def passing_vote(test_game, count):
    for i in range(1, count+1):
        player_id = "test_player_" + str(i)
        test_game.vote(player_id, "y")


def game_round(test_game, player_count, president_id, chancellor_id, policy):
    test_game.nominate(chancellor_id)
    passing_vote(test_game, player_count)
    test_game.discard_policy(president_id, policy)
    test_game.discard_policy(chancellor_id, policy)


if __name__ == "__main__":
    unittest.main()
