class MinimaxFixedDepthAgent:
    def __init__(self, game, heuristic, max_depth, chance_policy=None):
        self.game = game
        self.maximising_player = None
        self.heuristic = heuristic
        self.max_depth = max_depth
        self.chance_policy = chance_policy

    def check_if_maximising(self, game):
        return game.current_player.value == self.maximising_player.value

    def chance_node(self, game, is_maximising, current_depth):
        outcomes = self.chance_policy.get_outcomes(game)

        if outcomes is None or len(outcomes) == 0:
            return self.heuristic.evaluate(game, is_maximising)

        scores = 0
        for outcome in outcomes:
            next_is_maximising = self.check_if_maximising(outcome)
            score = self.minimax(outcome, next_is_maximising, current_depth)
            scores += score

        return scores / len(outcomes)

    def minimax(self, game, is_maximising, current_depth):
        if game.check_end():
            winner = game.check_victory()
            if winner == self.maximising_player.value:
                return 1
            elif winner is None:
                return 0
            else:
                return -1

        if game.chance_node_required():
            if self.chance_policy is None:
                raise ValueError("Chance policy required to evaluate chance nodes.")
            return self.chance_node(game, is_maximising, current_depth)

        if current_depth >= self.max_depth:
            return self.heuristic.evaluate(game, is_maximising)

        scores = []
        for move in game.get_legal_actions():
            cloned_game = game.clone()
            cloned_game.apply_deterministic_move(move)
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

        if self.chance_policy is not None:
            self.chance_policy.start_search()

        possible_moves = game.get_legal_actions()
        scores = []
        for move in possible_moves:
            cloned_game = game.clone()
            cloned_game.apply_deterministic_move(move)
            is_maximising = self.check_if_maximising(cloned_game)
            score = self.minimax(cloned_game, is_maximising, 1)
            scores.append((score, move))

        best_score, best_move = max(scores, key=lambda x: x[0])
        return best_move
