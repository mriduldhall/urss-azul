from .wall import Wall
from .tiles import Tiles
from .floor_line import FloorLine
from .pattern_line import PatternLine

class PlayerBoard:
    def __init__(self, value):
        self.value = value
        self.score = 0
        self.bonus_score = 0
        self.pattern_lines = [
            PatternLine(size) for size in range(1, 6)
        ]
        self.wall = Wall()
        self.floor = FloorLine()

    def get_score(self):
        return self.score + self.bonus_score

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
                score, bonus = self.wall.place_tile(i, colour)
                self.score += score
                self.bonus_score += bonus
                discard.extend([colour] * number)
        self.score -= self.floor.points_lost()
        if self.score <= 0:
            self.score = 0
        discard.extend(self.floor.clear())
        return discard

    def clone(self):
        clone = PlayerBoard(self.value)
        clone.score = self.score
        clone.bonus_score = self.bonus_score
        clone.pattern_lines = [pattern_line.clone() for pattern_line in self.pattern_lines]
        clone.wall = self.wall.clone()
        clone.floor = self.floor.clone()
        return clone

    def __eq__(self, other: object):
        if not isinstance(other, PlayerBoard):
            return False
        return (self.value == other.value and
                self.score == other.score and
                self.bonus_score == other.bonus_score and
                self.pattern_lines == other.pattern_lines and
                self.wall == other.wall and
                self.floor == other.floor)
