import random
from typing import List
from player import Player
from card import Card
from round import Round

class Game:
    CARD_TOKENS: List[str] = ["X", "O", "^"]
    CARD_NUMERIC_VALUES: List[int] = list(range(1, 9))
    CARDS_PER_PLAYER: int = 6
    NUMBER_OF_OPPONENTS: int = 3

    def __init__(self, player_name: str, total_rounds: int):
        self.create_players(player_name, Game.NUMBER_OF_OPPONENTS)
        self._human_player: Player = self._players[0]
        self._opponents: List[Player] = self._players[1:]

        self.create_cards(Game.CARD_TOKENS, Game.CARD_NUMERIC_VALUES)
        self.deal_cards()
        self._total_rounds = total_rounds

    def create_players(self, player_name: str, number_of_opponents: int):
        """
        Creates the list of players
        """
        self._players: List[Player] = []
        self._human_player: Player = Player(player_name, True)
        self._players.append(self._human_player)
        for i in range(1, number_of_opponents + 1):
            is_intelligent = random.choice([True, False])
            self._players.append(Player("Opponent " + str(i) + (" (Smart)" if is_intelligent else ""), False, is_intelligent))
    
    def create_cards(self, card_tokens: List[str], card_numeric_values: List[int]):
        """
        Creates and shuffles the deck of cards.
        """
        self._cards = []
        for card_token in card_tokens:
            for card_numeric_value in card_numeric_values:
                self._cards.append(Card(card_token, card_numeric_value))
        random.shuffle(self._cards)

    def deal_cards(self):
        """Deals the cards to the players"""
        number_of_card_being_dealt = 1
        current_player_index = 0
        for card in self._cards:
            if number_of_card_being_dealt > Game.CARDS_PER_PLAYER:
                break
            player: Player = self._players[current_player_index]
            player.add_card(card)
            if (current_player_index == len(self._players)-1):
                number_of_card_being_dealt += 1
                current_player_index = 0
            else:
                current_player_index += 1

    def play(self):
        for i in range(1, self._total_rounds + 1):
            print("~"*5 + f"Round {i}")
            game_round: Round = Round(Game.CARD_TOKENS, self._players, self._human_player, self._opponents)
            game_round.play()
        self.end()

    def end(self):
        print("\nThe game has ended. Here are the scores in descending order: ")
        players_sorted_by_score_desc = sorted(self._players, key=lambda player: player.score, reverse=True)
        for player in players_sorted_by_score_desc:
            print(f"Player: {player.name} -- {player.score}")

    @property
    def players(self) -> List[Player]:
        return self._players
    
    @property
    def human_player(self) -> Player:
        return self._human_player
    
    @property
    def opponents(self) -> List[Player]:
        return self._opponents