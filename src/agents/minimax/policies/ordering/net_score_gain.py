class NetScoreGainPolicy:
    @staticmethod
    def score(game, move):
        cloned_game = game.clone()
        player = cloned_game.current_player
        old_score = player.get_score()
        cloned_game.apply_deterministic_move(move)
        player.resolve_round()
        score_gain = player.get_score() - old_score
        return score_gain
