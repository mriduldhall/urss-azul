from time import perf_counter

#noinspection DuplicatedCode
class MinimaxIterativeDeepeningAgent:
    def __init__(self, game, heuristic, time_limit, max_depth, chance_policy=None, ordering_policy=None):
        self.game = game
        self.maximising_player = None
        self.heuristic = heuristic
        self.time_limit = time_limit
        self.max_depth = max_depth
        self.chance_policy = chance_policy
        self.ordering_policy = ordering_policy

    def check_if_maximising(self, game):
        return game.current_player.value == self.maximising_player.value

    def chance_node(self, game, max_depth, deadline, is_maximising, current_depth, chance_depth):
        if perf_counter() > deadline:
            raise TimeoutError("Time limit exceeded.")

        outcomes = self.chance_policy.get_outcomes(game, chance_depth)

        if outcomes is None or len(outcomes) == 0:
            return self.heuristic.evaluate(game, is_maximising)

        scores = 0
        for outcome in outcomes:
            next_is_maximising = self.check_if_maximising(outcome)
            score = self.minimax(outcome, max_depth, deadline, next_is_maximising, current_depth, chance_depth + 1)
            scores += score

        return scores / len(outcomes)

    def minimax(self, game, max_depth, deadline, is_maximising, current_depth, chance_depth, alpha=float('-inf'), beta=float('inf')):
        if perf_counter() > deadline:
            raise TimeoutError("Time limit exceeded.")

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
            return self.chance_node(game.clone(), max_depth, deadline, is_maximising, current_depth, chance_depth)

        if current_depth >= max_depth:
            return self.heuristic.evaluate(game, is_maximising)

        possible_moves = game.get_legal_actions()
        if self.ordering_policy is not None:
            possible_moves = sorted(
                possible_moves,
                key=lambda possible_move: self.ordering_policy.score(game, possible_move),
                reverse=True
            )

        best = float('-inf') if is_maximising else float('inf')
        for move in possible_moves:
            cloned_game = game.clone()
            cloned_game.apply_deterministic_move(move)
            next_is_maximising = self.check_if_maximising(cloned_game)
            score = self.minimax(cloned_game, max_depth, deadline, next_is_maximising, current_depth + 1, chance_depth, alpha, beta)
            if is_maximising:
                best = max(best, score)
                alpha = max(alpha, best)
            else:
                best = min(best, score)
                beta = min(beta, best)
            if alpha >= beta:
                break

        if is_maximising:
            return best
        else:
            return best

    def minimax_root(self, max_depth, deadline):
        if perf_counter() > deadline:
            raise TimeoutError("Time limit exceeded.")

        game = self.game.clone()
        self.maximising_player = game.current_player

        possible_moves = game.get_legal_actions()
        if self.ordering_policy is not None:
            possible_moves = sorted(
                possible_moves,
                key=lambda possible_move: self.ordering_policy.score(game, possible_move),
                reverse=True
            )

        scores = []
        alpha = float('-inf')
        for move in possible_moves:
            cloned_game = game.clone()
            cloned_game.apply_deterministic_move(move)
            is_maximising = self.check_if_maximising(cloned_game)
            score = self.minimax(cloned_game, max_depth, deadline, is_maximising, 1, 0, alpha)
            alpha = max(alpha, score)
            scores.append((score, move))

        best_score, best_move = max(scores, key=lambda x: x[0])
        return best_move

    def make_move(self):
        deadline = perf_counter() + self.time_limit
        best_move = None

        if self.chance_policy is not None:
            self.chance_policy.start_search()

        depth = 1
        while depth <= self.max_depth:
            try:
                move = self.minimax_root(depth, deadline)
            except TimeoutError:
                break
            best_move = move
            depth += 1

        return best_move
