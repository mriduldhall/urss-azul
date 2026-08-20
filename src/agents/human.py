class HumanAgent:
    def __init__(self, game):
        self.game = game

    def make_move(self):
        move = input("Please enter your move player " + self.game.current_player.value + ": ")
        success = False
        while not success:
            legal_moves = self.game.get_legal_actions()
            legal_moves = [str(move) for move in legal_moves]
            if move in legal_moves:
                success = True
            else:
                print("Invalid move. Please try again.")
                move = input("Please enter your move player " + self.game.current_player.value + ": ")
        return move