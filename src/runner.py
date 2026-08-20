class Runner:
    def __init__(self, game, player_one_agent, player_two_agent):
        self.game = game
        self.player_one_agent = player_one_agent
        self.player_two_agent = player_two_agent

    def run_game(self):
        end = self.game.check_end()
        while not end:
            print(self.game.display_board())
            if self.game.current_player == self.game.player_one_marker:
                move = self.player_one_agent.make_move()
            else:
                move = self.player_two_agent.make_move()
            self.game.make_move(move)
            end = self.game.check_end()
        print(self.game.display_board())
        winner = self.game.check_victory()
        if winner:
            print(f"Player {winner.value} wins!")
        else:
            print("It's a tie!")
