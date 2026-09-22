from environments.tic_tac_toe.game import Marker

class TicTacToeStateEncoder:
    @staticmethod
    def encode(game):
        encoded_state = ""
        for cell in game.board:
            if cell is game.current_player:
                encoded_state += "1"
            elif cell is Marker.EMPTY:
                encoded_state += "0"
            else:
                encoded_state += "-1"
        return encoded_state
