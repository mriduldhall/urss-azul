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

    def generate_seed(self, depth, sample_index):
        return f"{self.seed}:{depth}:{sample_index}"

    @staticmethod
    def generate_sample(game, rng):
        game.rng = rng
        game.bag.rng = rng
        game.bag.tiles.sort(key=lambda x: x.value)
        game.bag.discard.sort(key=lambda x: x.value)
        game.bag.rng.shuffle(game.bag.tiles)
        game.resolve_chance()

    def get_outcomes(self, game, depth):
        if self.seed is None:
            raise ValueError("start_search() must be called before get_outcomes().")

        outcomes = []
        for sample_index in range(self.samples):
            sample_seed = self.generate_seed(depth, sample_index)
            game_clone = game.clone()
            self.generate_sample(game_clone, Random(sample_seed))
            outcomes.append(game_clone)

        return outcomes
