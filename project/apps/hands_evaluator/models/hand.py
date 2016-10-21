from apps.hands_evaluator.services.dealer_service import DealerService
from apps.hands_evaluator.models import Card
from apps.hands_evaluator.models.histogram import Histogram


class Hand(object):
    HAND_STATUS_TIE = 1
    HAND_STATUS_WINNER = 2
    HAND_STATUS_LOOSER = 3

    HAND_STATUS_OPTIONS = (
        (HAND_STATUS_TIE, 'Tie'),
        (HAND_STATUS_WINNER, 'I\'m the winner!'),
        (HAND_STATUS_LOOSER, 'I loose'),
    )

    def __init__(self, deck=None):
        self.deck = deck
        self.status = Hand.HAND_STATUS_TIE
        self.cards = []
        self.suits = Histogram()
        self.numbers = Histogram()
        self.combinations = []

        cards_from_deck = DealerService.get_cards_from_deck(self.deck.token)
        for card_from_deck in cards_from_deck:
            card = Card(
                hand=self,
                suit_name=card_from_deck['suit'],
                number_name=card_from_deck['number'])
            self.cards.append(card)

            # Calculate histograms
            self.suits.count(card.suit)
            self.numbers.count(card.number)

        self.sets = self.numbers.values()
        self.sets = sorted(self.sets, reverse=True)

    def __str__(self):
        for status_value, status_name in Hand.HAND_STATUS_OPTIONS:
            if status_value == self.status:
                return '{}'.format(status_name)

    # TODO: DRY
    def __gt__(self, other):
        self_sorted_combinations = sorted(self.combinations, reverse=True)
        other_sorted_combinations = sorted(other.combinations, reverse=True)

        for combination_order, self_combination in enumerate(self_sorted_combinations):
            if not self._has_combination_in_this_order(combination_order, other_sorted_combinations):
                return True

            if self_combination > other_sorted_combinations[combination_order]:
                return True

        return False

    # TODO: DRY
    def __lt__(self, other):
        self_sorted_combinations = sorted(self.combinations, reverse=True)
        other_sorted_combinations = sorted(other.combinations, reverse=True)

        for combination_order, self_combination in enumerate(self_sorted_combinations):
            if not self._has_combination_in_this_order(combination_order, other_sorted_combinations):
                return False

            if self_combination < other_sorted_combinations[combination_order]:
                return True

        return False

    def _has_combination_in_this_order(self, combination_order, combinations):
        return (combination_order + 1) <= len(combinations)
