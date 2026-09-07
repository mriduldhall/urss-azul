from .bag import Bag
from .tiles import Tiles
from .centre import Centre
from .factory import Factory
from .player_board import PlayerBoard
from interfaces.azul_renderer import AzulRenderer
from .azul_move import SourceType, DestinationType, AzulMove

class Game:
    def __init__(self, initialise=True):
        self.bag = Bag()
        self.factories = [Factory() for _ in range(5)]
        self.centre = Centre()
        self.player_one = PlayerBoard(1)
        self.player_two = PlayerBoard(2)
        self.current_player = self.player_one
        self.renderer = AzulRenderer(self)
        if initialise:
            self.initialise_game()

    def get_legal_actions(self):
        legal_actions = []
        for factory_index, factory in enumerate(self.factories):
            for tile in set(factory.tiles):
                for pattern_line_index in range(5):
                    pattern_line =  self.current_player.pattern_lines[pattern_line_index]
                    wall_index = self.current_player.wall.PATTERN[pattern_line_index].index(tile)
                    if not pattern_line.is_complete() and (pattern_line.get_colour() is None or pattern_line.get_colour() == tile) and not self.current_player.wall.grid[pattern_line_index][wall_index]:
                        legal_actions.append(AzulMove(SourceType.FACTORY, factory_index, tile, DestinationType.PATTERN_LINE, pattern_line_index))
                legal_actions.append(AzulMove(SourceType.FACTORY, factory_index, tile, DestinationType.FLOOR_LINE, 0))

        if not self.centre.check_empty():
            for tile in set(self.centre.tiles):
                if tile == Tiles.STARTING:
                    continue
                for pattern_line_index in range(5):
                    pattern_line = self.current_player.pattern_lines[pattern_line_index]
                    wall_index = self.current_player.wall.PATTERN[pattern_line_index].index(tile)
                    if not pattern_line.is_complete() and (pattern_line.get_colour() is None or pattern_line.get_colour() == tile) and not self.current_player.wall.grid[pattern_line_index][wall_index]:
                        legal_actions.append(AzulMove(SourceType.CENTER, 0, tile, DestinationType.PATTERN_LINE, pattern_line_index))
                legal_actions.append(AzulMove(SourceType.CENTER, 0, tile, DestinationType.FLOOR_LINE, 0))

        return legal_actions

    def initialise_game(self):
        self.bag.initialise_bag()
        for factory in self.factories:
            for _ in range(4):
                factory.add_tile(self.bag.draw_tile())
        self.centre.reset_centre()

    def check_round_end(self):
        return all(factory.is_empty() for factory in self.factories) and self.centre.check_empty()

    def complete_round_end(self):
        if self.player_one.next_starting_player():
            self.current_player = self.player_two #Inverted since players switched again later
        elif self.player_two.next_starting_player():
            self.current_player = self.player_one

        discard = self.current_player.resolve_round()
        for tile in discard:
            self.bag.discard_tile(tile)

        other_player = self.player_one if self.current_player is self.player_two else self.player_two
        discard = other_player.resolve_round()
        for tile in discard:
            self.bag.discard_tile(tile)

    def setup_next_round(self):
        if self.bag.check_empty() and not self.bag.check_discard_empty():
            self.bag.shuffle_bag()

        for factory in self.factories:
            for _ in range(4):
                if self.bag.check_empty() and not self.bag.check_discard_empty():
                    self.bag.shuffle_bag()
                if not self.bag.check_empty():
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

        if move.source_type is SourceType.FACTORY:
            while not source.is_empty():
                tile = source.tiles[0]
                number = source.get_tile(source.tiles[0])
                for _ in range(number):
                    self.centre.add_tile(tile)

        if self.check_round_end():
            self.complete_round_end()
            if not (self.player_one.wall.check_end() or self.player_two.wall.check_end()):
                self.setup_next_round()

        self.current_player = self.player_one if self.current_player is self.player_two else self.player_two

    def check_victory(self):
        if (self.player_one.wall.check_end() or self.player_two.wall.check_end()) and self.check_round_end():
            if self.player_one.score > self.player_two.score:
                return self.player_one.value
            elif self.player_two.score > self.player_one.score:
                return self.player_two.value
            elif self.player_one.wall.completed_rows() > self.player_two.wall.completed_rows():
                return self.player_one.value
            elif self.player_two.wall.completed_rows() > self.player_one.wall.completed_rows():
                return self.player_two.value
        return None

    def check_end(self):
        victory = self.check_victory()
        if victory is not None:
            return True
        elif ((self.player_one.score == self.player_two.score) and
              (self.player_one.wall.check_end() or self.player_two.wall.check_end()) and self.check_round_end()):
            return True
        return False

    def clone(self):
        clone = Game(initialise=False)
        clone.bag = self.bag.clone()
        clone.factories = [factory.clone() for factory in self.factories]
        clone.centre = self.centre.clone()
        clone.player_one = self.player_one.clone()
        clone.player_two = self.player_two.clone()
        clone.current_player = clone.player_one if self.current_player is self.player_one else clone.player_two
        clone.renderer = AzulRenderer(clone)
        return clone

    def display_game(self):
        return self.renderer.render()
