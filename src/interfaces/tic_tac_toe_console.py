class TicTacToeInputHandler:
    def __init__(self, game):
        self.game = game

    def get_input(self):
        while True:
            try:
                row = int(input("Player " + self.game.current_player.value + ", please enter your row number: "))
                column = int(input("Player " + self.game.current_player.value + ", please enter your column number: "))
                return row, column
            except (ValueError, TypeError):
                print("Invalid input. Please enter valid integers.")

    def get_move(self):
        while True:
            row, column = self.get_input()
            move = ((row * 3) + column) - 4
            legal_moves = self.game.get_legal_actions()
            if move in legal_moves:
                return move
            else:
                print("Invalid move. Please try again.")
