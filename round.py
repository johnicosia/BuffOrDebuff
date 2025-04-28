from typing import List
from typing import Tuple
import random
from player import Player
from card import Card

class Round:
    """
    A class representing a round in the game.
    """
    def __init__(self, card_tokens: List[str], players: List[Player], human_player: Player, opponents: List[Player]):
        self._buff: str = random.choice(card_tokens)
        self._debuff: str = self._buff
        # Ensure that the debuff and buff are not the same tokens
        while self._buff == self._debuff:
            self._debuff = random.choice(card_tokens)
        self._debuffers: List[Player] = []
        self._players: List[Player] = players
        self._human_player: Player = human_player
        self._opponents: List[Player] = opponents

    def play(self):
        """
        Plays a round.
        """
        # display info
        self.display_round_info(self._players)
        self.display_players_cards(self._human_player)
        played_cards: List[Tuple[Player, Card]] = []

        # human player plays card
        played_cards.append((self._human_player, self.get_card_player_played(self._human_player)))

        # opponents randomly choose a card
        # TODO make this intelligent
        for player in self._opponents:
            card_to_play: Card = random.choice(player.get_cards())
            played_cards.append((player, card_to_play))

        # calculate the results
        winning_player_card_list: List[Tuple[Player, Card]] = []
        for player, card_played in played_cards:
            print(f"Player {player.name} played card {card_played.token} {card_played.numeric_value}")

            if (card_played.token == self._debuff):
                self._debuffers.append(player)

            if len(winning_player_card_list) == 0:
                winning_player_card_list.append((player, card_played))
            else:
                compare_result: int = self.compare_cards(winning_player_card_list[0][1], card_played)
                if compare_result == 1:
                    winning_player_card_list.clear()
                    winning_player_card_list.append((player, card_played))
                elif compare_result == 0:
                    winning_player_card_list.append((player, card_played))
        print("")

        # calculate the score(s)
        for winning_player, winning_card in winning_player_card_list:
            winning_card_score = winning_card.get_adjusted_numeric_value(self._buff)
            number_of_debuffers = len(self._debuffers)
            # remove debuffer if winner used a debuff
            if winning_player in self._debuffers:
                number_of_debuffers -= 1
            adjusted_winning_card_score = max(winning_card_score - (number_of_debuffers * 2), 0)
            print(f"{winning_player.name} Scored {adjusted_winning_card_score} points\n")
            winning_player.update_score(adjusted_winning_card_score)

    def get_card_player_played(self, human_player: Player) -> Card:
        players_cards: List[Card] = human_player.get_cards()
        # ask what card to play
        valid_card_index = False
        while valid_card_index == False:
            card_index_input = input("What card would you like to play? ")
            try:
                card_index = int(card_index_input)
            except:
                print("Invalid card choice...")
                continue
            if card_index < 0 or card_index > len(players_cards) - 1:
                print("Invalid card choice...")
                continue
            
            valid_card_index = True
        card_to_play: Card = players_cards[card_index]
        human_player.play_card(card_to_play)
        return card_to_play

    def display_players_scores(self, players: List[Player]):
        # Display Names and Scores
        name_score: str = ""
        for player in players:
            name_score += f"{player.score_string()}   "
        print(name_score)

    def display_round_info (self, players: List[Player]):
        self.display_players_scores(players)
        # Display buff and debuff
        print(f"Buff: {self._buff}  Debuff: {self._debuff}")

    def display_players_cards(self, human_player: Player):
        # Cheating but logic is the human player is in the first spot
        human_player: Player = human_player
        players_cards_for_round: List[Card] = human_player.get_cards()
        for card_index, card in enumerate(players_cards_for_round):
            print(f"{card_index}) {card.token} {card.numeric_value}")
        
    def compare_cards(self, card_a: Card, card_b: Card) -> int:
        """
        Compares two cards and returns -1 if card_b is less than card_a and 0 if they are equal in value or 1 if card_b is greater than card_a.
        """
        card_a_adjusted_value = card_a.get_adjusted_numeric_value(self._buff)
        
        card_b_adjusted_value = card_b.get_adjusted_numeric_value(self._buff)

        if card_a_adjusted_value < card_b_adjusted_value:
            return 1
        
        if card_a_adjusted_value > card_b_adjusted_value:
            return -1
        
        # If the values are the same see if either card's token is buff to break the tie
        if card_a_adjusted_value == card_b_adjusted_value:
            if card_a.token == self._buff:
                return -1
            elif card_b.token == self._buff:
                return 1
        
        return 0