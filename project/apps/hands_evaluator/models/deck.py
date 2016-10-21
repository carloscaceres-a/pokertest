from apps.hands_evaluator.services.dealer_service import DealerService
from apps.hands_evaluator.services.hand_ranker import HandRanker
from apps.hands_evaluator.models.hand import Hand
from django.apps import apps as django_apps


class Deck(object):
    def __init__(self, token=None):
        if token is None:
            token = DealerService.get_deck_token()

        self.token = token
        self.hands = None

    def __str__(self):
        return self.token

    def get_next_hands(self):
        config = django_apps.get_app_config('hands_evaluator')

        self.hands = []
        for hand_number in range(0, config.HANDS_NUMBER_PER_DEAL):
            hand = Hand(deck=self)
            hand = HandRanker.rank_hand(hand)
            self.hands.append(hand)

        sorted_hands = sorted(self.hands, reverse=True)
        for hand_order, hand in enumerate(sorted_hands):
            if (hand_order + 1) >= len(sorted_hands):
                break

            next_hand = sorted_hands[hand_order + 1]
            if hand.status == Hand.HAND_STATUS_LOOSER:  # There is a winner already
                next_hand.status = Hand.HAND_STATUS_LOOSER

            elif hand > next_hand:
                hand.status = Hand.HAND_STATUS_WINNER
                next_hand.status = Hand.HAND_STATUS_LOOSER

            elif hand > next_hand:
                hand.status = Hand.HAND_STATUS_TIE
                next_hand.status = Hand.HAND_STATUS_TIE

        return self.hands
