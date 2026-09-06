from environments.azul.tiles import Tiles
from environments.azul.azul_move import AzulMove, SourceType, DestinationType

class AzulInputHandler:
    TILE_MAP = {
        "T": Tiles.TURQUOISE,
        "Y": Tiles.YELLOW,
        "R": Tiles.RED,
        "B": Tiles.BLACK,
        "W": Tiles.WHITE,
    }

    def __init__(self, game):
        self.game = game

    def get_input(self):
        while True:
            print("Player " + str(self.game.current_player.value) + "'s turn.")

            try:
                source = input("Enter the row number (1-5) of the factory or C for centre: ")
                if source.upper() == "C":
                    source_type = SourceType.CENTER
                    source_index = 0
                else:
                    source_type = SourceType.FACTORY
                    source_index = int(source) - 1

                tile = input("Enter the tile colour (T, Y, R, B, W): ").upper()
                if tile in self.TILE_MAP:
                    tile = self.TILE_MAP[tile]
                else:
                    raise ValueError("Invalid tile colour.")

                destination = input("Enter the pattern line number (1-5) or F for floor line: ")
                if destination.upper() == "F":
                    destination_type = DestinationType.FLOOR_LINE
                    destination_index = 0
                else:
                    destination_type = DestinationType.PATTERN_LINE
                    destination_index = int(destination) - 1

                return source_type, source_index, tile, destination_type, destination_index
            except (ValueError, TypeError):
                print("Invalid input. Please enter valid options.")

    def get_move(self):
        while True:
            source_type, source_index, tile, destination_type, destination_index = self.get_input()
            move = AzulMove(source_type, source_index, tile, destination_type, destination_index)
            legal_moves = self.game.get_legal_actions()
            if move in legal_moves:
                return move
            else:
                print("Invalid move. Please try again.")
