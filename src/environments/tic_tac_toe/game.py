from enum import Enum

class Marker(Enum):
    X = 'X'
    O = 'O'
    EMPTY = ' '


class Game:
    def __init__(self):
        self.player_one_marker = Marker.X
        self.player_two_marker = Marker.O
        self.current_player = self.player_one_marker
        self.board = [Marker.EMPTY] * 9

    def get_legal_actions(self):
        return [position for position, marker in enumerate(self.board) if marker is Marker.EMPTY]

    def make_move(self, position):
        if position not in self.get_legal_actions():
            return None
        self.board[position] = self.current_player
        self.current_player = self.player_two_marker if self.current_player is self.player_one_marker else self.player_one_marker
        return True

    def check_victory(self):
        possible_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for combination in possible_combinations:
            if self.board[combination[0]] == self.board[combination[1]] == self.board[combination[2]] != Marker.EMPTY:
                return self.board[combination[0]]
        return None

    def display_board(self):
        return f"{self.board[0].value} | {self.board[1].value} | {self.board[2].value}\n" \
               f"---------\n" \
               f"{self.board[3].value} | {self.board[4].value} | {self.board[5].value}\n" \
               f"---------\n" \
               f"{self.board[6].value} | {self.board[7].value} | {self.board[8].value}\n"
