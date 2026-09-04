from tiles import Tiles

class Centre:
    def __init__(self):
        self.tiles = [Tiles.STARTING]

    def reset_centre(self):
        self.tiles = [Tiles.STARTING]

    def check_empty(self):
        return len(self.tiles) == 0

    def check_starting_tile(self):
        return Tiles.STARTING in self.tiles

    def remove_starting_tile(self):
        if not self.check_starting_tile():
            raise ValueError("Starting tile not found in centre.")
        self.tiles.remove(Tiles.STARTING)

    def add_tile(self, tile):
        if not isinstance(tile, Tiles):
            raise ValueError("Invalid tile. Must be an instance of Tiles Enum.")
        if tile is Tiles.STARTING:
            raise ValueError("Cannot re-add starting tile.")
        self.tiles.append(tile)

    def get_tile(self, tile):
        if tile not in self.tiles:
            raise ValueError("Tile not found in factory.")
        if len(self.tiles) == 0:
            raise ValueError("Factory is empty. No tiles to retrieve.")
        if self.check_starting_tile():
            raise ValueError("Cannot retrieve tiles when starting tile is present.")
        number = self.tiles.count(tile)
        self.tiles = [i for i in self.tiles if i != tile]
        return number
