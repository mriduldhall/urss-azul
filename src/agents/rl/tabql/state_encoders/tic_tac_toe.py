from environments.tic_tac_toe.game import Marker

class TicTacToeStateEncoder:
    @staticmethod
    def encode(game):
        encoded_state = []
        for cell in game.board:
            if cell is game.current_player:
                encoded_state.append(1)
            elif cell is Marker.EMPTY:
                encoded_state.append(0)
            else:
                encoded_state.append(-1)
        return tuple(encoded_state)
