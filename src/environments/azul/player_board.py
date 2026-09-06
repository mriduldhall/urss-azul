from .wall import Wall
from .tiles import Tiles
from .floor_line import FloorLine
from .pattern_line import PatternLine

class PlayerBoard:
    def __init__(self, value):
        self.value = value
        self.score = 0
        self.pattern_lines = [
            PatternLine(size) for size in range(1, 6)
        ]
        self.wall = Wall()
        self.floor = FloorLine()

    def next_starting_player(self):
        return self.floor.first_player_tile()

    def place_tiles(self, pattern_line_index, tile, number, starting_tile=False, floor_line=False):
        if (pattern_line_index < 0 or pattern_line_index >= len(self.pattern_lines)) and not floor_line:
            raise ValueError("Invalid pattern line index.")
        if floor_line:
            self.floor.add_tiles(tile, number)
            overflow = 0
        else:
            overflow = self.pattern_lines[pattern_line_index].add_tiles(tile, number)
        if starting_tile:
            self.floor.add_tiles(Tiles.STARTING, 1)
        if overflow > 0:
            self.floor.add_tiles(tile, overflow)

    def resolve_round(self):
        discard = []
        for i, pattern_line in enumerate(self.pattern_lines):
            if pattern_line.is_complete():
                number, colour = pattern_line.clear()
                self.wall.place_tile(i, colour)
                self.score += self.wall.calculate_score(i, self.wall.PATTERN[i].index(colour))
                discard.extend([colour] * number)
        self.score -= self.floor.points_lost()
        discard.extend(self.floor.clear())
        return discard
