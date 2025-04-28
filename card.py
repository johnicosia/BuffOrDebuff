class Card:
    """
    A class representing a card in the game.
    """
    def __init__(self, token: str, numeric_value: int):
        """
        Initializes the card.
        """
        self._token: str = token
        self._numeric_value: int = numeric_value

    @property
    def token(self) -> str:
        """
        Returns the token value of the card.
        """
        return self._token

    @property
    def numeric_value(self) -> int:
        """
        Returns the numeric value of the card.
        """
        return self._numeric_value

    def get_adjusted_numeric_value(self, buff: str):
        """
        Returns the adjusted numeric value of the card depending on what token is buffed.
        """
        if self._token == buff:
            return self._numeric_value + 2
        return self._numeric_value
    
