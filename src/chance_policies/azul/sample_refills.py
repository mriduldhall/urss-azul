from random import Random

class SampleRefillsPolicy:
    def __init__(self, samples=1, rng=None):
        if samples < 1:
            raise ValueError("Number of samples must be at least 1.")
        self.samples = samples
        self.rng = rng if rng is not None else Random()
        self.seed = None

    def start_search(self):
        self.seed = self.rng.getrandbits(128)

    def get_outcomes(self, game):
        if self.seed is None:
            raise ValueError("start_search() must be called before get_outcomes().")
        return None
