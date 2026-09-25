class OutcomeReward:
    @staticmethod
    def get_reward(game, acting_player):
        if not game.check_end():
            return 0

        victor = game.check_victory()
        if victor is None:
            return 0
        elif victor == acting_player.value:
            return 1
        return -1

    @staticmethod
    def get_config():
        return "terminal-outcome"
