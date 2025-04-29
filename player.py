from typing import List
from typing import Dict
import itertools
from card import Card

class Player:
    """
    A class representing a player in the game.
    """
    def __init__(self, name: str, is_human:bool, is_intelligent: bool = False):
        """
        Initializes the player.
        """
        self._name = name
        self._cards: Dict[str, List[Card]] = dict()
        self._score = 0
        self._is_human = is_human
        self._is_intelligent = is_intelligent

    @property
    def name(self) -> str:
        """
        Returns the name of the player.
        """
        return self._name
    
    def add_card(self, card: Card):
        """
        Adds a card to the player's hand.
        """
        if card.token in self._cards:
            self._cards[card.token].append(card)
        else:
            self._cards[card.token] = [card]

    def play_card(self, card: Card):
        """
        Removes the card played.
        """
        self._cards[card.token].remove(card)

    @property
    def cards(self) -> Dict[str, List[Card]]:
        """
        Returns player's cards grouped by token
        """
        return self._cards

    def get_cards(self, token: str) -> List[Card]:
        """
        Gets all the cards that the player has for a particular token.
        """
        if token in self._cards:
            return self._cards[token]
        else:
            return []
    
    def get_all_cards(self) -> List[Card]:
        """
        Returns a list of all the cards the player has.
        """
        return list(itertools.chain(*list(self._cards.values())))
    
    def update_score(self, value_added_to_score):
        """
        Updates the player's score.
        """
        self._score = self._score + value_added_to_score
    
    @property
    def score(self) -> int:
        """
        Returns the player's score.
        """
        return self._score
    
    def score_string(self) -> str:
        """
        Returns string containing the players_name: players_score
        """
        # Display Names and Scores
        return f"{self._name}: {self._score}"
    
    @property
    def is_human(self) -> bool:
        """
        Returns if the player is human or not
        """
        return self._is_human
    
    @property
    def is_intelligent(self) -> bool:
        """
        Returns if the player (who is not played by a human is using logic to play a card)
        """
        return self._is_intelligent
