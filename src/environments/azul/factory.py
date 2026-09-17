from .tiles import Tiles

class Factory:
    def __init__(self):
        self.tiles = []

    def is_empty(self):
        return len(self.tiles) == 0

    def add_tile(self, tile):
        if not isinstance(tile, Tiles):
            raise ValueError("Invalid tile. Must be an instance of Tiles Enum.")
        if tile is Tiles.STARTING:
            raise ValueError("Cannot add a starting tile to the factory.")
        if len(self.tiles) >= 4:
            raise ValueError("Factory can only hold a maximum of 4 tiles.")
        self.tiles.append(tile)

    def get_tile(self, tile):
        if tile not in self.tiles:
            raise ValueError("Tile not found in factory.")
        if len(self.tiles) == 0:
            raise ValueError("Factory is empty. No tiles to retrieve.")
        number = self.tiles.count(tile)
        self.tiles = [i for i in self.tiles if i != tile]
        return number

    def clone(self):
        clone = Factory()
        clone.tiles = self.tiles.copy()
        return clone

    def __eq__(self, other: object):
        if not isinstance(other, Factory):
            return False
        return self.tiles == other.tiles
