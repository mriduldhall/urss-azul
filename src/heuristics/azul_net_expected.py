class AzulNetExpectedHeuristic:
    @staticmethod
    def evaluate(game, is_maximising):
        game = game.clone()
        if is_maximising:
            max_player = game.current_player
            min_player = game.player_one if game.current_player is game.player_two else game.player_two
        else:
            max_player = game.player_one if game.current_player is game.player_two else game.player_two
            min_player = game.current_player

        max_player.resolve_round()
        max_player_score = max_player.score
        min_player.resolve_round()
        min_player_score = min_player.score
        return max_player_score - min_player_score
