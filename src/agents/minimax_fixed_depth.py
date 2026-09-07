class MinimaxFixedDepthAgent:
    def __init__(self, game, heuristic, max_depth):
        self.game = game
        self.maximising_player = None
        self.heuristic = heuristic
        self.max_depth = max_depth

    def check_if_maximising(self, game):
        return game.current_player.value == self.maximising_player.value

    def minimax(self, game, is_maximising, current_depth):
        if game.check_end():
            winner = game.check_victory()
            if winner == self.maximising_player.value:
                return float('inf')
            elif winner is None:
                return 0
            else:
                return -float('inf')

        if current_depth >= self.max_depth:
            return self.heuristic.evaluate(game, is_maximising)

        scores = []
        for move in game.get_legal_actions():
            cloned_game = game.clone()
            cloned_game.make_move(move)
            next_is_maximising = self.check_if_maximising(cloned_game)
            score = self.minimax(cloned_game, next_is_maximising, current_depth + 1)
            scores.append(score)

        if is_maximising:
            return max(scores)
        else:
            return min(scores)

    def make_move(self):
        game = self.game.clone()
        self.maximising_player = game.current_player

        possible_moves = game.get_legal_actions()
        scores = []
        for move in possible_moves:
            cloned_game = game.clone()
            cloned_game.make_move(move)
            is_maximising = self.check_if_maximising(cloned_game)
            score = self.minimax(cloned_game, is_maximising, 1)
            scores.append((score, move))

        best_score, best_move = max(scores, key=lambda x: x[0])
        return best_move
