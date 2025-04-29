from typing import List
from typing import Dict
import itertools
import random
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

    def play_card(self, buff: str, debuff: str) -> Card:
        """
        The player plays a card.
        """
        if self.is_human:
            return self._human_play_card()
        else:
            return self._ai_play_card(buff, debuff)

    def _human_play_card(self):
        players_cards: List[Card] = self.get_all_cards()
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
        self._cards[card_to_play.token].remove(card_to_play)
        return card_to_play

    def _ai_play_card(self, buff: str, debuff: str):
        if self.is_intelligent == False:
            card_to_play = random.choice(self.get_all_cards())
        else:
            # look at buffed cards
            cards_by_token: Dict[str, List[Card]] = self.cards
            if buff in cards_by_token:
                buff_cards: List[Card] = cards_by_token[buff]
            else:
                buff_cards: List[Card] = []
            if debuff in cards_by_token:
                debuff_cards: List[Card] = cards_by_token[debuff]
            else:
                debuff_cards: List[Card] = []
            buff_and_debuff_cards: List[Card] = buff_cards + debuff_cards
            sorted_buff_and_debuff_cards = sorted(buff_and_debuff_cards, key=lambda card: card.get_adjusted_numeric_value(buff), reverse=True)
            # if no cards with buff/debuff choose the highest value
            if len(sorted_buff_and_debuff_cards) == 0:
                sorted_cards = sorted(self.get_all_cards(), key=lambda card: card.get_adjusted_numeric_value(buff), reverse=True)
                card_to_play = sorted_cards[0]
            else:
                # Choose the highest value of the buff or debuff cards
                highest_buff_card: Card = None
                highest_debuff_card: Card = None
                for card in sorted_buff_and_debuff_cards:
                    if card.token == buff:
                        if highest_buff_card == None:
                            highest_buff_card = card
                            continue
                    if card.token == debuff:
                        if highest_debuff_card == None:
                            highest_debuff_card = card
                            continue
                    # done searching when found the highest debuff and buff card
                    if highest_buff_card != None and highest_debuff_card != None:
                        break
                if highest_buff_card is None:
                    card_to_play = highest_debuff_card
                elif highest_debuff_card is None:
                    card_to_play = highest_buff_card
                elif highest_buff_card.get_adjusted_numeric_value(buff) > highest_debuff_card.get_adjusted_numeric_value(buff) + 2:
                    card_to_play = highest_buff_card
                else:
                    card_to_play = highest_debuff_card
        self._cards[card_to_play.token].remove(card_to_play)
        return card_to_play

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
