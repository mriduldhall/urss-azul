from environments.azul.tiles import Tiles

class AzulStateEncoder:
    def encode(self, game):
        encoded_state = ""
        encoded_state += self.encode_factories(game.factories)
        encoded_state += "||"
        encoded_state += self.encode_centre(game.centre)
        encoded_state += "||"
        current_player_board = game.current_player
        other_player = game.player_one if game.current_player is game.player_two else game.player_two
        encoded_state += self.encode_board(current_player_board)
        encoded_state += "||"
        encoded_state += self.encode_board(other_player)
        return encoded_state

    @staticmethod
    def encode_factory(factory):
        encoded_factory = ""
        tiles = sorted(factory.tiles, key=lambda x: x.value)
        for tile in tiles:
            encoded_factory += tile.value
        return encoded_factory

    def encode_factories(self, factories):
        encoded_factories = ""
        factory_number = 1
        for factory in factories:
            encoded_factories += self.encode_factory(factory)
            if factory_number < len(factories):
                encoded_factories += "|"
            factory_number += 1
        return encoded_factories

    @staticmethod
    def encode_centre(centre):
        encoded_centre = ""
        tiles = sorted(centre.tiles, key=lambda x: x.value)
        for tile in tiles:
            encoded_centre += tile.value
        return encoded_centre

    @staticmethod
    def encode_board(board):
        encoded_board = ""
        for index, pattern_line in enumerate(board.pattern_lines):
            tile = (pattern_line.colour.value if pattern_line.colour else "0")
            for _ in range(pattern_line.count):
                encoded_board += tile
            encoded_board += "."

            wall_line = board.wall.grid[index]
            for wall_tile in wall_line:
                encoded_board += "1" if wall_tile else "0"
            encoded_board += "|"

        encoded_board += str(len(board.floor.tiles))
        if Tiles.STARTING in board.floor.tiles:
            encoded_board += "1"

        return encoded_board

    @staticmethod
    def get_config():
        return "azul-relative-current-player"
