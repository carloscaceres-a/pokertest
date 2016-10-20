class Card(object):
    CARD_SUIT_HEARTS = 0
    CARD_SUIT_DIAMONDS = 1
    CARD_SUIT_CLUBS = 2
    CARD_SUIT_SPADES = 3

    CARD_SUIT_OPTIONS = (
        (CARD_SUIT_HEARTS, 'Hearts'),
        (CARD_SUIT_DIAMONDS, 'Diamonds'),
        (CARD_SUIT_CLUBS, 'Clubs'),
        (CARD_SUIT_SPADES, 'Spades'),
    )

    CARD_NUMBER_A = 1
    CARD_NUMBER_2 = 2
    CARD_NUMBER_3 = 3
    CARD_NUMBER_4 = 4
    CARD_NUMBER_5 = 5
    CARD_NUMBER_6 = 6
    CARD_NUMBER_7 = 7
    CARD_NUMBER_8 = 8
    CARD_NUMBER_9 = 9
    CARD_NUMBER_10 = 10
    CARD_NUMBER_J = 11
    CARD_NUMBER_Q = 12
    CARD_NUMBER_K = 13

    CARD_NUMBER_OPTIONS = (
        (CARD_NUMBER_A, 'A'),
        (CARD_NUMBER_2, '2'),
        (CARD_NUMBER_3, '3'),
        (CARD_NUMBER_4, '4'),
        (CARD_NUMBER_5, '5'),
        (CARD_NUMBER_6, '6'),
        (CARD_NUMBER_7, '7'),
        (CARD_NUMBER_8, '8'),
        (CARD_NUMBER_9, '9'),
        (CARD_NUMBER_10, '10'),
        (CARD_NUMBER_J, 'J'),
        (CARD_NUMBER_Q, 'Q'),
        (CARD_NUMBER_K, 'K'),
    )

    def __init__(
            self,
            hand=None,
            suit_name=None,
            number_name=None):
        self.hand = hand
        self.suit_name = suit_name
        self.number_name = number_name
        self.suit = self._load_suit_from_name()
        self.number = self._load_number_from_name()

    def __str__(self):
        return '{} of {}'.format(self.suit_name, self.number_name)

    def _load_suit_from_name(self):
        for suit_value, suit_name in Card.CARD_SUIT_OPTIONS:
            if suit_name.lower() == self.suit_name.lower():
                return suit_value

        raise ValueError('Invalid suit name')

    def _load_number_from_name(self):
        for number_value, number_name in Card.CARD_NUMBER_OPTIONS:
            if number_name.lower() == self.number_name.lower():
                return number_value

        raise ValueError('Invalid number name')

    def __cmp__(self, other):
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return cmp(t1, t2)
