from enum import Enum

class Marker(Enum):
    X = 'X'
    O = 'O'
    EMPTY = ' '


class Game:
    max_possible_score = 1
    min_possible_score = -1

    def __init__(self):
        self.player_one = Marker.X
        self.player_two = Marker.O
        self.current_player = self.player_one
        self.board = [Marker.EMPTY] * 9

    @staticmethod
    def chance_node_required():
        return False

    def get_legal_actions(self):
        return [position for position, marker in enumerate(self.board) if marker is Marker.EMPTY]

    def apply_deterministic_move(self, position):
        return self.make_move(position)

    def make_move(self, position):
        if self.check_end():
            raise ValueError("Game has already ended. No more moves can be made.")

        try:
            position = int(position)
        except (ValueError, TypeError):
            raise ValueError("Invalid move. Position must be an integer.")

        if position not in self.get_legal_actions():
            raise ValueError("Invalid move. Position is either occupied or out of bounds.")

        self.board[position] = self.current_player
        self.current_player = self.player_two if self.current_player is self.player_one else self.player_one
        return True

    def check_victory(self):
        possible_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for combination in possible_combinations:
            if self.board[combination[0]] == self.board[combination[1]] == self.board[combination[2]] != Marker.EMPTY:
                return self.board[combination[0]].value
        return None

    def check_end(self):
        if self.check_victory() is not None:
            return True
        if not self.get_legal_actions():
            return True
        return False

    def clone(self):
        cloned_game = Game()
        cloned_game.board = self.board.copy()
        cloned_game.player_one = self.player_one
        cloned_game.player_two = self.player_two
        cloned_game.current_player = self.current_player
        return cloned_game

    def display_game(self):
        return f"{self.board[0].value} | {self.board[1].value} | {self.board[2].value}\n" \
               f"---------\n" \
               f"{self.board[3].value} | {self.board[4].value} | {self.board[5].value}\n" \
               f"---------\n" \
               f"{self.board[6].value} | {self.board[7].value} | {self.board[8].value}\n"
