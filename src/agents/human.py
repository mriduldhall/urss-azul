class HumanAgent:
    def __init__(self, input_handler):
        self.input_handler = input_handler

    def make_move(self):
        move = self.input_handler.get_move()
        return move
