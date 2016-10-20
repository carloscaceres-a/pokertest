from apps.hands_evaluator.models import Combination


class HandRanker(object):
    @classmethod
    def rank_hand(cls, hand):
        combinations_names = Combination.get_combinations_names()
        for combinations_name in combinations_names:
            combination_check_function = getattr(
                HandRanker, 'has_' + combinations_name)

            combination = combination_check_function(hand)
            if combination is not False:
                hand.combinations.append(combination)

        return hand

    @classmethod
    def has_highcard(cls, hand):
        if len(hand.cards):
            highest_number = -1
            for card in hand.cards:
                if card.number > highest_number:
                    highest_number = card.number

        combination = Combination(name='highcard', value=highest_number)
        return combination

    @classmethod
    def check_sets(cls, hand, *t):
        for need, have in zip(t, hand.sets):
            if need > have:
                return False

        return True

    @classmethod
    def has_pair(cls, hand):
        if cls.check_sets(hand, 2):
            return Combination(name='pair')
        return False

    @classmethod
    def has_twopair(cls, hand):
        if cls.check_sets(hand, 2, 2):
            return Combination(name='twopair')
        return False

    @classmethod
    def has_threekind(cls, hand):
        if cls.check_sets(hand, 3):
            return Combination(name='threekind')
        return False

    @classmethod
    def has_fourkind(cls, hand):
        if cls.check_sets(hand, 4):
            return Combination(name='fourkind')
        return False

    @classmethod
    def has_fullhouse(cls, hand):
        if cls.check_sets(hand, 3, 2):
            return Combination(name='fullhouse')
        return False

    @classmethod
    def has_flush(cls, hand):
        for val in hand.suits.values():
            if val >= 5:
                return Combination(name='flush')
        return False

    @classmethod
    def has_straight(cls, hand):
        numbers = hand.numbers.copy()
        numbers[14] = numbers.get(1, 0)

        if cls.in_a_row(hand, numbers, 5):
            return Combination(name='straight')

        return False

    @classmethod
    def in_a_row(cls, hand, numbers, n):
        count = 0
        for i in range(1, 15):
            if numbers.get(i, 0):
                count += 1
                if count == 5:
                    return True
            else:
                count = 0

        return False

    @classmethod
    def has_straightflush(cls, hand):
        # make a set of the (number, suit) pairs we have
        s = set()
        for c in hand.cards:
            s.add((c.number, c.suit))
            if c.number == 1:
                s.add((14, c.suit))

        # iterate through the suits and numbers and see if we
        # get to 5 in a row
        for suit in range(4):
            count = 0
            for number in range(1, 15):
                if (number, suit) in s:
                    count += 1
                    if count == 5:
                        return Combination(name='straightflush')
                else:
                    count = 0

        return False

# @classmethod
# def has_straightflush(cls, hand):
#     """Checks whether this hand has a straight flush.

#     Better algorithm (in the sense of being more demonstrably
#     correct).
#     """
#     # partition the hand by suit and check each
#     # sub-hand for a straight
#     d = {}
#     for c in hand.cards:
#         d.setdefault(c.suit, PokerHand()).add_card(c)

#     # see if any of the partitioned hands has a straight
#     for hand in d.values():
#         if len(hand.cards) < 5:
#             continue
#         hand.make_histograms()
#         if hand.has_straight():
#             return True
#     return False

# @classmethod
# def classify(cls, hand):
#     hand.make_histograms()

#     hand.labels = []
#     for label in HandRanker.all_labels:
#         f = getattr(hand, 'has_' + label)
#         if f():
#             hand.labels.append(label)

# def main(*args):
#     deck = Deck()
#     deck.shuffle()

#     for i in range(10):
#         hand = PokerHand()
#         deck.move_cards(hand, 5) #add cards
#         hand.classify()

#         for label in hand.labels:
#             print(label)


# the label histogram: map from label to number of occurances
# lhist = Hist()

# loop n times, dealing 7 hands per iteration, 7 cards each
# n = 10000
# for i in range(n):
#     if i%1000 == 0:
#         print(i)

#     deck = PokerDeck()
#     deck.shuffle()

#     hands = deck.deal_hands(7, 7)
#     for hand in hands:
#         for label in hand.labels:
#             lhist.count(label)

# # print the results
# total = 7.0 * n
# print(total, 'hands dealt:')

# for label in PokerHand.all_labels:
#     freq = lhist.get(label, 0)
#     if freq == 0:
#         continue
#     p = total / freq
#     print('%s happens one time in %.2f' % (label, p))
