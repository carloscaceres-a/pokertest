class Combination(object):
    COMBINATION_HIGH_CARD = 0
    COMBINATION_ONE_PAIR = 1
    COMBINATION_TWO_PAIRS = 2
    COMBINATION_THREE_OF_A_KIND = 3
    COMBINATION_STRAIGHT = 4
    COMBINATION_FLUSH = 5
    COMBINATION_FULL_HOUSE = 6
    COMBINATION_FOUR_OF_A_KIND = 7
    COMBINATION_STRAIGHT_FLUSH = 8

    COMBINATIONS_OPTIONS = (
        (COMBINATION_HIGH_CARD, 'highcard'),
        (COMBINATION_ONE_PAIR, 'pair'),
        (COMBINATION_TWO_PAIRS, 'twopair'),
        (COMBINATION_THREE_OF_A_KIND, 'threekind'),
        (COMBINATION_STRAIGHT, 'straight'),
        (COMBINATION_FLUSH, 'flush'),
        (COMBINATION_FULL_HOUSE, 'fullhouse'),
        (COMBINATION_FOUR_OF_A_KIND, 'fourkind'),
        (COMBINATION_STRAIGHT_FLUSH, 'straightflush'),
    )

    def __init__(self, name=None, value=-1):
        self.name = name
        self.weight = -1
        self.value = value

        if name is not None:
            self.weight = self._load_weight_from_name()

    def __str__(self):
        if self.value != -1:
            return '{} {} ({})'.format(self.weight, self.name, self.value)
        else:
            return '{} {}'.format(self.weight, self.name)

    def __cmp__(self, other):
        t1 = self.weight, self.value
        t2 = other.weight, other.value
        return cmp(t1, t2)

    # TODO: DRY
    def __gt__(self, other):
        if self.weight > other.weight:
            return True
        elif self.weight == other.weight:
            if self.value > other.value:
                return True

        return False

    # TODO: DRY
    def __lt__(self, other):
        if self.weight < other.weight:
            return True
        elif self.weight == other.weight:
            if self.value < other.value:
                return True

        return False

    def _load_weight_from_name(self):
        for weight_value, weight_name in Combination.COMBINATIONS_OPTIONS:
            if weight_name.lower() == self.name.lower():
                return weight_value

        raise ValueError('Invalid combination name')

    @classmethod
    def get_combinations_names(cls):
        return [option[1] for option in Combination.COMBINATIONS_OPTIONS]
