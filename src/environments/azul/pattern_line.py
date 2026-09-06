class PatternLine:
    def __init__(self, size):
        self.size = size
        self.count = 0
        self.colour = None

    def is_complete(self):
        return self.count == self.size

    def get_colour(self):
        return self.colour

    def add_tiles(self, tile, number):
        if self.is_complete():
            raise ValueError("Pattern line is already complete.")
        if self.colour is not None and self.colour != tile:
            raise ValueError("Cannot add different coloured tiles to the same pattern line.")
        overflow = self.count + number - self.size
        if overflow <= 0:
            overflow = 0
        self.colour = tile
        self.count += number
        if self.count > self.size:
            self.count = self.size
        return overflow

    def clear(self):
        if not self.is_complete():
            raise ValueError("Pattern line is not complete.")
        number = self.count
        colour = self.colour
        self.count = 0
        self.colour = None
        return number - 1, colour

    def clone(self):
        clone = PatternLine(self.size)
        clone.count = self.count
        clone.colour = self.colour
        return clone
