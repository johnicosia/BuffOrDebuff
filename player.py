from typing import List
from card import Card

class Player:
    """
    A class representing a player in the game.
    """
    def __init__(self, name: str):
        """
        Initializes the player.
        """
        self._name = name
        self._cards = []
        self._score = 0

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
        self._cards.append(card)

    def play_card(self, card: Card):
        """
        Removes the card played.
        """
        self._cards.remove(card)

    def get_cards(self) -> List[Card]:
        """
        Gets all the cards that the player has.
        """
        return self._cards
    
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
