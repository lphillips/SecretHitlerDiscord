import random
from enum import Enum
from PIL import Image
from secret_hitler import config, images


class IllegalStateTransition(Exception):
    pass


class GameState(Enum):
    GAME_STARTING = 1
    NOMINATION = 2
    ELECTION = 3
    LEGISLATIVE_PRESIDENT = 4
    LEGISLATIVE_CHANCELLOR = 5
    GOVERNMENT_IN_CHAOS = 6
    VETO = 7
    INVESTIGATION = 8
    SPECIAL_ELECTION = 9
    POLICY_PEEK = 10
    EXECUTION = 11
    GAME_OVER = 12


class VoteResult(Enum):
    CHANCELLOR_ELECTED = 1
    CHANCELLOR_REJECTED = 2
    GOVERNMENT_IN_CHAOS = 3
    VALID = 4
    INVALID = 5
    NO_ELECTION = 6


class Player:
    def __init__(self, player_id, display_name, avatar_url):
        self.player_id = player_id
        self.role = None
        self.dead = False
        self.display_name = display_name
        self.avatar_url = avatar_url

    def get_id(self):
        return self.player_id

    def get_party(self):
        if self.role == 'Hitler' or self.role == 'Fascist':
            return 'Fascist'
        else:
            return 'Liberal'


class Game:

    def __init__(self, observer, channel_id, game_id, max_players, admin_id):
        self.observer = observer
        self._president_ = None
        self.chancellor = None
        self.nominated = None
        self._special_election_president_ = None
        self.winner = None
        self.prev_president = None
        self.prev_chancellor = None
        self.liberal_board = 0
        self.fascist_board = 0
        self.failed_votes = 0
        self.channel_id = channel_id
        self.admin_id = admin_id
        self.max_players = max_players
        self.game_id = game_id
        self.deck = ['L', 'L', 'L', 'L', 'L', 'L', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F']
        self.discard = []
        self.nominated = None
        self.policies = []
        self.investigated_one = False
        self.investigated = False
        self.peeked = False
        self.executed_one = False
        self.executed_two = False
        random.shuffle(self.deck)
        self.players = {}
        self.play_order = []
        self.dead = []
        self.state = GameState.GAME_STARTING
        self.votes = {}

    @property
    def current_president(self) -> Player:
        if self._special_election_president_ is not None:
            return self._special_election_president_
        else:
            return self._president_

    def __transition_to_state(self, next_state, ctx=None):
        prev_state = self.state
        self.state = next_state
        if self.state == GameState.GAME_STARTING:
            self.__start_game()
            self.observer.on_enter_game_start(self, ctx)

            # GAME_STARTING is the start state where we do set up.
            # Set up is done and the observer has been notified, so
            # enter the first actual game state.
            self.__transition_to_state(GameState.NOMINATION)
        elif self.state == GameState.NOMINATION:
            if prev_state != GameState.SPECIAL_ELECTION:
                self.set_president()
                self._special_election_president_ = None
            self.observer.on_enter_nomination(self, ctx)
        elif self.state == GameState.ELECTION:
            self.observer.on_enter_election(self, self.nominated, ctx)
        elif self.state == GameState.LEGISLATIVE_PRESIDENT:
            self.__president_legislative()
            self.observer.on_enter_legislative_president(self, ctx)
        elif self.state == GameState.LEGISLATIVE_CHANCELLOR:
            self.__chancellor_legislative()
            self.observer.on_enter_legislative_chancellor(self, ctx)
        elif self.state == GameState.GOVERNMENT_IN_CHAOS:
            self.__government_in_chaos()
        elif self.state == GameState.VETO:
            # TODO: Determine what should happen here
            self.observer.on_enter_veto(self, ctx)
        elif self.state == GameState.INVESTIGATION:
            # TODO: Determine what should happen here
            self.observer.on_enter_investigation(self, ctx)
        elif self.state == GameState.SPECIAL_ELECTION:
            # TODO: Determine what should happen here
            self.observer.on_enter_special_election(self, ctx)
        elif self.state == GameState.POLICY_PEEK:
            self.__policy_peek()
            self.observer.on_enter_policy_peek(self, ctx)
        elif self.state == GameState.EXECUTION:
            # TODO: Determine what should happen here
            self.observer.on_enter_execution(self, ctx)
        elif self.state == GameState.GAME_OVER:
            # TODO: Determine what should happen here
            self.observer.on_enter_game_over(self, ctx)
        else:
            raise ValueError("Unknown GameState encountered")

    def __is_player_president(self, player_id) -> bool:
        if self.current_president is None:
            return False
        return self.current_president.get_id() == player_id

    def __is_player_chancellor(self, player_id) -> bool:
        if self.chancellor is None:
            return False
        return self.chancellor.player_id == player_id

    def __is_player_previous_president(self, player_id) -> bool:
        if self.prev_president is None:
            return False
        return self.prev_president.get_id() == player_id

    def __is_player_previous_chancellor(self, player_id) -> bool:
        if self.prev_chancellor is None:
            return False
        return self.prev_chancellor.player_id == player_id

    def add_player(self, player_id, display_name, avatar_url):
        if len(self.players) == self.max_players:
            return False
        if self.get_player(player_id) is not None:
            return False
        self.players[player_id] = Player(player_id, display_name, avatar_url)
        self.play_order.append(self.players[player_id])

        return True

    def start_game(self) -> bool:
        if len(self.players) < self.max_players:
            return False

        self.__transition_to_state(GameState.GAME_STARTING)
        return True

    def __start_game(self):
        # Shuffle seats
        random.shuffle(self.play_order)

        # Shuffle roles
        roles = config.configuration[self.max_players]["roles"]
        random.shuffle(roles)

        for index, player in enumerate(self.players.values()):
            player.role = roles[index]

    def nominate(self, player_id, ctx=None):
        player = self.get_player(player_id)
        if self.__is_player_eligible_for_nomination(player_id):
            self.nominated = player
            self.__transition_to_state(GameState.ELECTION, ctx=ctx)
            return True
        else:
            return False

    def __is_player_eligible_for_nomination(self, player_id: str) -> bool:
        # Eligibility rules:
        # 1. The last elected president and chancellor are ineligible to be chancellor.
        # 2. If there are only five players left in the game, the last elected president
        #    becomes eligible to be chancellor.
        # 3. TODO: Veto power and the election tracker state can affect eligibility

        player_num = len(self.players)
        if player_num <= 5:
            if self.__is_player_chancellor(player_id):
                return False
        elif player_num > 5:
            if self.__is_player_chancellor(player_id) or self.__is_player_previous_president(player_id):
                return False

        if self.__is_player_president(player_id):
            return False
        # All eligibility tests passed. This candidate is eligible.
        return True

    def vote(self, player_id: str, vote: str) -> VoteResult:
        if self.state != GameState.ELECTION:
            # TODO: We could raise an exception here and rely on the app module to ignore voting if no election is in process
            return VoteResult.NO_ELECTION

        is_vote_valid = self.__count_vote(player_id, vote)

        if not is_vote_valid:
            return VoteResult.INVALID

        # If all votes are in, process the result of the election
        if len(self.votes) == len(self.players):
            vote_passed = self.__calculate_votes()
            next_state = self.__next_state_after_vote(vote_passed)
            self.__transition_to_state(next_state)
            if vote_passed:
                return VoteResult.CHANCELLOR_ELECTED
            elif next_state == GameState.GAME_OVER:
                # Secret Hitler was elected; bad show
                return VoteResult.CHANCELLOR_ELECTED
            elif next_state == GameState.GOVERNMENT_IN_CHAOS:
                return VoteResult.GOVERNMENT_IN_CHAOS
            else:
                return VoteResult.CHANCELLOR_REJECTED
        else:
            # Intermediate vote counted; election not over
            return VoteResult.VALID

    def __count_vote(self, player_id, vote):
        if self.get_player(player_id) is None:
            return False

        for pid, s_v in self.votes.items():
            if pid == player_id:
                return False

        if len(self.votes) == len(self.players):
            return False

        self.votes[player_id] = vote
        return True

    def __calculate_votes(self):
        yes = 0
        no = 0
        for _, vote in self.votes.items():
            if vote == 'y':
                yes = yes + 1
            elif vote == 'n':
                no = no + 1

        self.votes = {}

        vote_passed = yes > no
        if vote_passed:
            if self.chancellor is not None:
                self.prev_chancellor = self.chancellor
                self.prev_chancellor_id = self.chancellor.player_id
            self.chancellor = self.nominated
        else:
            self.nominated = None
            self.failed_votes = self.failed_votes + 1
        return vote_passed

    def __next_state_after_vote(self, vote_passed: bool) -> GameState:
        if vote_passed:
            if self.chancellor.role == "Hitler" and self.fascist_board >= 3:
                self.winner = "Fascist"
                return GameState.GAME_OVER
            else:
                return GameState.LEGISLATIVE_PRESIDENT
        else:
            if self.failed_votes >= 3:
                # Government in chaos - the result of the random policy draw with determine the next state
                return GameState.GOVERNMENT_IN_CHAOS
            else:
                return GameState.NOMINATION

    def __next_state_for_placed_policy(self, new_policy: str) -> GameState:
        if new_policy == "L":
            if self.liberal_board >= 5:
                return GameState.GAME_OVER
            else:
                return GameState.NOMINATION
        else:
            if self.fascist_board >= 6:
                return GameState.GAME_OVER
            else:
                if self.fascist_board == 1 and not self.investigated_one and self.max_players > 8:
                    return GameState.INVESTIGATION
                if self.fascist_board == 2 and not self.investigated and self.max_players > 6:
                    return GameState.INVESTIGATION
                elif self.fascist_board == 3 and not self.peeked:
                    if self.max_players > 6:
                        return GameState.SPECIAL_ELECTION
                    else:
                        return GameState.POLICY_PEEK
                elif self.fascist_board == 4 and not self.executed_one:
                    return GameState.EXECUTION
                elif self.fascist_board == 5 and not self.executed_two:
                    return GameState.EXECUTION
                else:
                    # No special action activate; just move to the next round
                    return GameState.NOMINATION

    def __government_in_chaos(self):
        policy = self.draw_policy()
        next_state = self.place_policy(policy)
        self.failed_votes = 0
        self.__transition_to_state(next_state)

    def start_nomination(self):
        self.__transition_to_state(GameState.NOMINATION)

    def get_players(self):
        return self.players

    def get_id(self):
        return self.game_id

    def has_player(self, player_id):
        for player in self.players:
            if player_id == player.get_id():
                return True
        return False

    def get_player(self, player_id):
        return self.players.get(player_id)

    def return_path_to_fascist_board(self):
        if self.fascist_board == 0:
            if self.max_players < 7:
                return 'secret_hitler/img/FascistBoard1.png'
            elif self.max_players < 9:
                return 'secret_hitler/img/FascistBoard2.png'
            return 'secret_hitler/img/FascistBoard3.png'
        return "secret_hitler/img/fascist_" + str(self.game_id) + ".png"

    def return_path_to_liberal_board(self):
        if self.liberal_board == 0:
            return 'secret_hitler/img/LiberalBoard.png'
        return "secret_hitler/img/liberal_" + str(self.game_id) + ".png"

    def set_president(self):
        if self._president_ is None:
            self._president_ = self.play_order[0]
        else:
            president_index = self.play_order.index(self._president_)
            next_president_index = (president_index + 1) % len(self.play_order)
            self.prev_president = self.current_president
            self._president_ = self.play_order[next_president_index]

    def draw_policy(self):
        if len(self.deck) == 0:
            self.deck = self.discard.copy()
            self.discard.clear()
            random.shuffle(self.deck)
        return self.deck.pop(0)

    def place_policy(self, policy) -> GameState:
        if 'L' in policy:
            self.liberal_board = self.liberal_board + 1
        if 'F' in policy:
            self.fascist_board = self.fascist_board + 1

        next_state = self.__next_state_for_placed_policy(policy)
        if next_state == GameState.GAME_OVER:
            if self.liberal_board >= 5:
                self.winner = "Liberal"
            else:
                self.winner = "Fascist"
        return next_state

    def __president_legislative(self):
        policy1 = self.draw_policy()
        policy2 = self.draw_policy()
        policy3 = self.draw_policy()
        self.policies.append(policy1)
        self.policies.append(policy2)
        self.policies.append(policy3)

        policy_hand_image = images.PolicyHandImage([policy1, policy2, policy3])
        policy_hand_image.compose()
        policy_hand_image.write("secret_hitler/img/president_" + str(self.game_id) + ".png")

    def __policy_peek(self):
        policy1 = self.draw_policy()
        policy2 = self.draw_policy()
        policy3 = self.draw_policy()

        policy_hand_image = images.PolicyHandImage([policy1, policy2, policy3])
        policy_hand_image.compose()
        policy_hand_image.write("secret_hitler/img/policypeek_" + str(self.game_id) + ".png")

        self.deck.insert(0, policy3)
        self.deck.insert(0, policy2)
        self.deck.insert(0, policy1)

        self.peeked = True

    def finish_policy_peek(self):
        self.__transition_to_state(GameState.NOMINATION)

    def print_board(self):
        img1 = Image.open('secret_hitler/img/liberal_policy.png')

        img_new = Image.open('secret_hitler/img/LiberalBoard.png')
        for i in range(self.liberal_board):
            img_new.paste(img1, config.configuration["liberal_board"][i])
        img_new.save("secret_hitler/img/liberal_" + str(self.game_id) + ".png")

        img2 = Image.open('secret_hitler/img/fascist_policy.png')

        if self.max_players < 7:
            img_new_2 = Image.open('secret_hitler/img/FascistBoard1.png')
        elif self.max_players < 9:
            img_new_2 = Image.open('secret_hitler/img/FascistBoard2.png')
        else:
            img_new_2 = Image.open('secret_hitler/img/FascistBoard3.png')

        for i in range(self.fascist_board):
            img_new_2.paste(img2, config.configuration["fascist_board"][i])
        img_new_2.save("secret_hitler/img/fascist_" + str(self.game_id) + ".png")

    def __chancellor_legislative(self):
        policy1 = self.policies[0]
        policy2 = self.policies[1]

        policy_hand_image = images.PolicyHandImage([policy1, policy2])
        policy_hand_image.compose()
        policy_hand_image.write("secret_hitler/img/chancellor_" + str(self.game_id) + ".png")

    def discard_policy(self, player_id, discard_policy):
        discard_policy = discard_policy.upper()

        if self.__is_valid_discard(player_id, discard_policy):
            try:
                discard_index = self.policies.index(discard_policy)
            except ValueError:
                # Attempted to discard a policy not in hand
                return False

            popped = self.policies[discard_index]
            self.policies.pop(discard_index)
            self.discard.append(popped)

            if len(self.policies) == 1:
                next_state = self.place_policy(self.policies[0])
                self.policies.clear()
                self.__transition_to_state(next_state)
            if len(self.policies) == 2:
                self.__transition_to_state(GameState.LEGISLATIVE_CHANCELLOR)

            return True
        else:
            return False

    def __is_valid_discard(self, player_id: str, policy: str) -> bool:
        if policy != "L" and policy != "F":
            return False

        if self.state == GameState.LEGISLATIVE_PRESIDENT and self.__is_player_president(player_id):
            return True
        elif self.state == GameState.LEGISLATIVE_CHANCELLOR and self.__is_player_chancellor(player_id):
            return True
        else:
            return False

    def __discard_all_policies(self):
        self.discard.extend(self.policies)
        self.policies.clear()

    def execute_player(self, player_id):
        player_to_execute = self.get_player(player_id)
        if player_to_execute is not None:
            self.__kill_player(player_to_execute)
            if self.fascist_board == 4:
                self.executed_one = True
            elif self.fascist_board == 5:
                self.executed_two = True

            if player_to_execute.role == "Hitler":
                self.__transition_to_state(GameState.GAME_OVER)
            else:
                self.__transition_to_state(GameState.NOMINATION)
            return player_to_execute
        else:
            return None

    def __kill_player(self, player):
        self.players.pop(player.get_id())
        index = self.play_order.index(player)
        self.play_order.pop(index)
        self.dead.append(player)

    def investigate_player(self, player_id):
        investigated_player = self.get_player(player_id)
        if investigated_player is not None:
            if self.investigated_one:
                self.investigated = True
            else:
                self.investigated_one = True
            self.__transition_to_state(GameState.NOMINATION)
            return investigated_player.get_party()
        return None

    def special_election(self, player_id):
        if self.__is_player_president(player_id):
            return False
        se_president = self.get_player(player_id)
        if se_president is not None:
            self._special_election_president_ = se_president
            self.__transition_to_state(GameState.NOMINATION)
            return True
        else:
            return False

    def request_veto(self, player_id: str) -> bool:
        if self.state != GameState.LEGISLATIVE_CHANCELLOR:
            return False
        if not self.__is_player_chancellor(player_id):
            return False

        self.__transition_to_state(GameState.VETO)
        return True

    def veto(self, player_id: str, accept_veto: bool) -> bool:
        if self.state != GameState.VETO:
            return False
        if not self.__is_player_president(player_id):
            return False

        if accept_veto:
            self.__discard_all_policies()
            self.failed_votes += 1
            if self.failed_votes >= 3:
                self.__transition_to_state(GameState.GOVERNMENT_IN_CHAOS)
            else:
                self.__transition_to_state(GameState.NOMINATION)
        else:
            self.__transition_to_state(GameState.LEGISLATIVE_CHANCELLOR)

        return True


    def restart_game(self):
        # TODO: reimplement restart in app as a creation of a new Game object
        pass

