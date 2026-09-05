from tiles import Tiles

class FloorLine:
    PENALTIES = (1, 1, 2, 2, 2, 3, 3)

    def __init__(self):
        self.tiles = []

    def first_player_tile(self):
        if Tiles.STARTING in self.tiles:
            return True
        return False

    def add_tiles(self, tile, number):
        self.tiles.extend([tile] * number)

    def points_lost(self):
        total_penalty = 0
        for i in range(min(len(self.tiles), len(self.PENALTIES))):
            total_penalty += self.PENALTIES[i]
        return total_penalty

    def clear(self):
        removed_tiles = self.tiles.copy()
        removed_tiles.remove(Tiles.STARTING)
        self.tiles.clear()
        return removed_tiles
