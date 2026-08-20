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

    def display_board(self):
        return f"{self.board[0].value} | {self.board[1].value} | {self.board[2].value}\n" \
               f"---------\n" \
               f"{self.board[3].value} | {self.board[4].value} | {self.board[5].value}\n" \
               f"---------\n" \
               f"{self.board[6].value} | {self.board[7].value} | {self.board[8].value}\n"
