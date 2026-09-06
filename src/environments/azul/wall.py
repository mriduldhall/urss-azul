from .tiles import Tiles

class Wall:
    PATTERN = (
        (Tiles.TURQUOISE, Tiles.YELLOW, Tiles.RED, Tiles.BLACK, Tiles.WHITE),
        (Tiles.WHITE, Tiles.TURQUOISE, Tiles.YELLOW, Tiles.RED, Tiles.BLACK),
        (Tiles.BLACK, Tiles.WHITE, Tiles.TURQUOISE, Tiles.YELLOW, Tiles.RED),
        (Tiles.RED, Tiles.BLACK, Tiles.WHITE, Tiles.TURQUOISE, Tiles.YELLOW),
        (Tiles.YELLOW, Tiles.RED, Tiles.BLACK, Tiles.WHITE, Tiles.TURQUOISE),
    )

    def __init__(self):
        self.grid = [[False for _ in range(5)] for _ in range(5)]

    def check_end(self):
        for row in self.grid:
            if all(row):
                return True
        return False

    def completed_rows(self):
        return sum(1 for row in self.grid if all(row))

    # noinspection DuplicatedCode
    def calculate_score(self, row, column):
        score = 0
        if self.grid[row][column]:
            score += 1

        row_start_score = score

        row_negative_indices = [i for i in range(column - 1, -1, -1)]
        for i in row_negative_indices:
            if self.grid[row][i]:
                score += 1
            else:
                break

        row_positive_indices = [i for i in range(column + 1, 5)]
        for i in row_positive_indices:
            if self.grid[row][i]:
                score += 1
            else:
                break

        row_bonus = score - row_start_score

        column_start_score = score

        column_negative_indices = [i for i in range(row - 1, -1, -1)]
        for i in column_negative_indices:
            if self.grid[i][column]:
                score += 1
            else:
                break

        column_positive_indices = [i for i in range(row + 1, 5)]
        for i in column_positive_indices:
            if self.grid[i][column]:
                score += 1
            else:
                break

        column_bonus = score - column_start_score

        if row_bonus > 0 and column_bonus > 0:
            score += 1

        return score

    def calculate_bonus(self, row, column):
        bonus = 0

        if all(self.grid[row]):
            bonus += 2

        if all(self.grid[i][column] for i in range(5)):
            bonus += 7

        tile_type = self.PATTERN[row][column]
        if all(self.grid[i][j] for i in range(5) for j in range(5) if self.PATTERN[i][j] == tile_type):
            bonus += 10

        return bonus

    def place_tile(self, pattern_line_index, tile):
        if pattern_line_index < 0 or pattern_line_index >= 5:
            raise ValueError("Invalid pattern line index. Must be between 0 and 4.")
        if tile not in Tiles:
            raise ValueError("Invalid tile. Must be an instance of Tiles Enum.")
        if tile == Tiles.STARTING:
            raise ValueError("Cannot place a starting tile on the wall.")

        row = pattern_line_index
        column = self.PATTERN[row].index(tile)

        if self.grid[row][column]:
            raise ValueError("Tile already placed in this position on the wall.")

        self.grid[row][column] = True
        return self.calculate_score(row, column) + self.calculate_bonus(row, column)
