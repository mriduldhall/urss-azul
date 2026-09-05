from bag import Bag
from centre import Centre
from factory import Factory
from player_board import PlayerBoard
from interfaces.azul_renderer import AzulRenderer

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

    def display_game(self):
        return self.renderer.render()


if __name__ == '__main__':
    game = Game()
    game.initialise_game()
    print(game.display_game())
