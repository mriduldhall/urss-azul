class HumanAgent:
    def __init__(self, game):
        self.game = game

    def make_move(self):
        move = input("Please enter your move: ")
        success = False
        while not success:
            if move in self.game.valid_moves:
                success = True
            else:
                print("Invalid move. Please try again.")
                move = input("Please enter your move: ")
        return move