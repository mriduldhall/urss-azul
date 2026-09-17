from environments.azul.tiles import Tiles
from environments.azul.azul_move import DestinationType, SourceType

#noinspection DuplicatedCode
class PointEpsilonPolicy:
    def __init__(self, epsilon=0.1):
        self.epsilon = epsilon

    @staticmethod
    def score_destination(game, move):
        if move.destination_type == DestinationType.FLOOR_LINE:
            if move.source_type == SourceType.FACTORY:
                return -1 * game.factories[move.source_index].tiles.count(move.tile)
            else:
                tiles = game.centre.tiles.count(move.tile)
                if Tiles.STARTING in game.centre.tiles:
                    tiles += 1
                return -1 * tiles
        return 0

    @staticmethod
    def score_row(game, move):
        if move.destination_type == DestinationType.FLOOR_LINE:
            return 0

        if move.source_type == SourceType.FACTORY:
            tiles = game.factories[move.source_index].tiles.count(move.tile)
        else:
            tiles = game.centre.tiles.count(move.tile)

        existing_tiles = game.current_player.pattern_lines[move.destination_index].count
        line_size = game.current_player.pattern_lines[move.destination_index].size

        completion = (existing_tiles + tiles) / line_size
        score = 0
        if completion >= 1:
            score = 3
            overflow = (existing_tiles + tiles) - line_size
            score += -1 * overflow
        return score

    @staticmethod
    def score_column(game, move):
        if move.destination_type == DestinationType.FLOOR_LINE:
            return 0

        column = game.current_player.wall.PATTERN[move.destination_index].index(move.tile)
        if column == 0 or column == 4:
            return 1
        elif column == 1 or column == 3:
            return 2
        else:
            return 3

    def score(self, game, move):
        score = 0
        score += self.score_destination(game, move)
        row_score = self.score_row(game, move)
        score += row_score
        score += self.score_column(game, move)
        return score

    def choose_move(self, game, moves, rng):
        if rng.random() < self.epsilon:
            return rng.choice(moves)

        scores = [self.score(game, move) for move in moves]
        best_score = max(scores)
        best_moves = [move for move, score in zip(moves, scores) if score == best_score]
        return rng.choice(best_moves)
