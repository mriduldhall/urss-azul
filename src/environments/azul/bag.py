from random import shuffle
from .tiles import Tiles

class Bag:
    def __init__(self):
        self.tiles = []
        self.discard = []

    def check_empty(self):
        return len(self.tiles) == 0

    def check_discard_empty(self):
        return len(self.discard) == 0

    def initialise_bag(self):
        if self.check_empty() and len(self.discard) == 0:
            for tile in Tiles:
                if tile is not Tiles.STARTING:
                    self.tiles.extend([tile] * 20)
            shuffle(self.tiles)

    def shuffle_bag(self):
        if not self.check_empty():
            raise ValueError("Bag still has tiles remaining. Cannot shuffle.")
        if len(self.discard) <= 0:
            raise ValueError("Discard pile is empty. Cannot shuffle.")
        self.tiles = self.discard.copy()
        self.discard.clear()
        shuffle(self.tiles)

    def draw_tile(self):
        if self.check_empty():
            raise ValueError("Bag is empty. Cannot draw a tile.")
        return self.tiles.pop()

    def discard_tile(self, tile):
        if not isinstance(tile, Tiles):
            raise ValueError("Invalid tile. Must be an instance of Tiles Enum.")
        self.discard.append(tile)
