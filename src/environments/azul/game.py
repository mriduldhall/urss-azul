from bag import Bag
from centre import Centre
from factory import Factory
from player_board import PlayerBoard

class Game:
    def __init__(self):
        self.bag = Bag()
        self.factories = [Factory() for _ in range(5)]
        self.centre = Centre()
        self.player_one = PlayerBoard()
        self.player_two = PlayerBoard()
        self.current_player = self.player_one

    def initialise_game(self):
        self.bag.initialise_bag()
        for factory in self.factories:
            for _ in range(4):
                factory.add_tile(self.bag.draw_tile())
        self.centre.reset_centre()
