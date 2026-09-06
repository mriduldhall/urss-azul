from bag import Bag
from centre import Centre
from factory import Factory
from player_board import PlayerBoard
from interfaces.azul_renderer import AzulRenderer
from azul_move import SourceType, DestinationType

class Game:
    def __init__(self):
        self.bag = Bag()
        self.factories = [Factory() for _ in range(5)]
        self.centre = Centre()
        self.player_one = PlayerBoard()
        self.player_two = PlayerBoard()
        self.current_player = self.player_one
        self.renderer = AzulRenderer(self)

    def initialise_game(self):
        self.bag.initialise_bag()
        for factory in self.factories:
            for _ in range(4):
                factory.add_tile(self.bag.draw_tile())
        self.centre.reset_centre()

    def make_move(self, move):
        if self.check_end():
            raise ValueError("Game has already ended. No more moves can be made.")

        starting = False
        if move.source_type is SourceType.FACTORY:
            source = self.factories[move.source_index]
        elif move.source_type is SourceType.CENTER:
            source = self.centre
            if source.check_starting_tile():
                source.remove_starting_tile()
                starting = True
        else:
            raise ValueError("Invalid source type.")

        floor = False
        if move.destination_type is DestinationType.FLOOR_LINE:
            floor = True
        elif move.destination_type is not DestinationType.PATTERN_LINE:
            raise ValueError("Invalid destination type.")

        tiles_taken = source.get_tile(move.tile)
        self.current_player.place_tiles(move.destination_index, move.tile, tiles_taken, starting, floor)

    def check_victory(self):
        if self.player_one.wall.check_end() or self.player_two.wall.check_end():
            if self.player_one.score > self.player_two.score:
                return 1
            elif self.player_two.score > self.player_one.score:
                return 2
        return None

    def check_end(self):
        if self.check_victory() is not None:
            return True
        elif self.player_one.score == self.player_two.score:
            return True
        return False

    def display_game(self):
        return self.renderer.render()
