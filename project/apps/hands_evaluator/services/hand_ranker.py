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
