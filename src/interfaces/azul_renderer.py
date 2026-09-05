import os
import re
import shutil

from src.environments.azul.tiles import Tiles


class AzulRenderer:
    RESET = "\033[0m"
    TILE_COLOURS = {
        Tiles.TURQUOISE.value: "\033[96m",
        Tiles.YELLOW.value: "\033[93m",
        Tiles.RED.value: "\033[91m",
        Tiles.BLACK.value: "\033[90m",
        Tiles.WHITE.value: "\033[97m",
        Tiles.STARTING.value: "\033[95m",
    }
    ANSI_PATTERN = re.compile(r"\033\[[0-9;]*m")
    PLAYER_GAP = 4

    def __init__(self, game):
        self.game = game
        self.use_colour = "NO_COLOR" not in os.environ

    def render(self):
        """Return the complete game state as a terminal-ready string."""
        terminal_width = shutil.get_terminal_size(fallback=(80, 24)).columns

        output = ["FACTORIES"]
        output.extend(self._render_factories(terminal_width))
        output.extend(("", self._render_centre(), ""))

        player_one = self._render_player(self.game.player_one, 1)
        player_two = self._render_player(self.game.player_two, 2)
        output.extend(self._join_player_boards(player_one, player_two, terminal_width))
        output.extend(("", "Wall: lowercase = empty target, uppercase = placed tile"))

        return "\n".join(output)

    def render_tile(self, tile, occupied=True):
        """Render one tile, using a lowercase letter for an empty wall target."""
        if tile is None:
            return "."

        symbol = getattr(tile, "value", None)
        if symbol not in self.TILE_COLOURS:
            raise ValueError("Invalid tile. Must be an instance of Tiles Enum.")

        symbol = symbol if occupied else symbol.lower()
        if not self.use_colour:
            return symbol

        colour = self.TILE_COLOURS[tile.value]
        if occupied:
            return f"{colour}{symbol}{self.RESET}"
        return f"\033[2m{colour}{symbol}{self.RESET}"

    def _render_factories(self, terminal_width):
        factories = []
        for index, factory in enumerate(self.game.factories, start=1):
            tiles = [self.render_tile(tile) for tile in factory.tiles]
            tiles.extend("." for _ in range(4 - len(tiles)))
            factories.append(f"F{index} [{' '.join(tiles)}]")

        rows = []
        current_row = ""
        for factory in factories:
            candidate = factory if not current_row else f"{current_row}   {factory}"
            if current_row and self._visible_length(candidate) > terminal_width:
                rows.append(current_row)
                current_row = factory
            else:
                current_row = candidate

        if current_row:
            rows.append(current_row)
        return rows

    def _render_centre(self):
        tiles = " ".join(self.render_tile(tile) for tile in self.game.centre.tiles)
        return f"CENTRE C [{tiles or 'empty'}]"

    def _render_player(self, board, player_number):
        current_marker = ">" if self.game.current_player is board else " "
        lines = [
            f"{current_marker} PLAYER {player_number} - Score: {board.score}",
            "  Pattern   | Wall",
        ]

        for row_index, pattern_line in enumerate(board.pattern_lines):
            unavailable_slots = [" "] * (5 - pattern_line.size)
            empty_slots = ["."] * (pattern_line.size - pattern_line.count)
            filled_slots = [
                self.render_tile(pattern_line.colour)
                for _ in range(pattern_line.count)
            ]
            pattern = " ".join(unavailable_slots + empty_slots + filled_slots)

            wall = " ".join(
                self.render_tile(tile, occupied=board.wall.grid[row_index][column])
                for column, tile in enumerate(board.wall.PATTERN[row_index])
            )
            lines.append(f"{row_index + 1} {pattern} | {wall}")

        penalties = " ".join(f"-{penalty}" for penalty in board.floor.PENALTIES)
        floor_tiles = [self.render_tile(tile) for tile in board.floor.tiles]
        visible_floor_tiles = floor_tiles[:len(board.floor.PENALTIES)]
        visible_floor_tiles.extend(
            "." for _ in range(len(board.floor.PENALTIES) - len(visible_floor_tiles))
        )
        floor = "  ".join(visible_floor_tiles)

        lines.append(f"Floor: {penalties}")
        floor_line = f"        {floor}"
        if len(floor_tiles) > len(board.floor.PENALTIES):
            floor_line += f"  (+{len(floor_tiles) - len(board.floor.PENALTIES)} excess)"
        lines.append(floor_line)
        return lines

    def _join_player_boards(self, left, right, terminal_width):
        left_width = max(self._visible_length(line) for line in left)
        right_width = max(self._visible_length(line) for line in right)
        combined_width = left_width + self.PLAYER_GAP + right_width

        if combined_width > terminal_width:
            return left + [""] + right

        number_of_rows = max(len(left), len(right))
        left.extend("" for _ in range(number_of_rows - len(left)))
        right.extend("" for _ in range(number_of_rows - len(right)))

        return [
            f"{self._pad_visible(left_line, left_width)}"
            f"{' ' * self.PLAYER_GAP}{right_line}"
            for left_line, right_line in zip(left, right)
        ]

    def _visible_length(self, text):
        return len(self.ANSI_PATTERN.sub("", text))

    def _pad_visible(self, text, width):
        return text + " " * (width - self._visible_length(text))
