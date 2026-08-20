class MinimaxAgent:
    def __init__(self, game):
        self.game = game
        self.maximising_player = None

    def minimax(self, game, is_maximising):
        if game.check_end():
            winner = game.check_victory()
            if winner == self.maximising_player:
                return float('inf')
            elif winner is None:
                return 0
            else:
                return -float('inf')

        scores = []
        for move in game.get_legal_actions():
            cloned_game = game.clone()
            cloned_game.make_move(move)
            score = self.minimax(cloned_game, not is_maximising)
            scores.append(score)

        if is_maximising:
            return max(scores)
        else:
            return min(scores)

    def make_move(self):
        game = self.game.clone()
        self.maximising_player = game.current_player

        maximising = True
        possible_moves = game.get_legal_actions()
        scores = []
        for move in possible_moves:
            cloned_game = game.clone()
            cloned_game.make_move(move)
            score = self.minimax(cloned_game, not maximising)
            scores.append((score, move))

        best_score, best_move = max(scores, key=lambda x: x[0])
        print(f"MinimaxAgent: Score {best_score}")
        return best_move
