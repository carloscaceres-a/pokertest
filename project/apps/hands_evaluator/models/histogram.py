class Histogram(dict):
    def __init__(self, seq=[]):
        for x in seq:
            self.count(x)

    def count(self, x, f=1):
        self[x] = self.get(x, 0) + f
        if self[x] == 0:
            del self[x]
