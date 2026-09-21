from random import Random

class SingleSamplePolicy:
    def __init__(self, rng=None):
        self.rng = rng if rng is not None else Random()

    #noinspection DuplicatedCode
    @staticmethod
    def generate_sample(game, rng):
        game.rng = rng
        game.bag.rng = rng
        game.bag.tiles.sort(key=lambda x: x.value)
        game.bag.discard.sort(key=lambda x: x.value)
        game.bag.rng.shuffle(game.bag.tiles)

    def sample_outcome(self, game):
        rng = Random(self.rng.getrandbits(128))
        self.generate_sample(game, rng)
        return game
