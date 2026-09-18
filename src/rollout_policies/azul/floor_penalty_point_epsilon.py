from environments.azul.tiles import Tiles
from environments.azul.azul_move import DestinationType, SourceType

#noinspection DuplicatedCode
class FloorPenaltyPointEpsilonPolicy:
    def __init__(self, epsilon=0.1):
        if epsilon < 0 or epsilon > 1:
            raise ValueError("Epsilon must be between 0 and 1.")
        self.epsilon = epsilon

    # @staticmethod
    # def score_column(game, move):
    #     if move.destination_type == DestinationType.FLOOR_LINE:
    #         return 0
    #
    #     column = game.current_player.wall.PATTERN[move.destination_index].index(move.tile)
    #     if column == 0 or column == 4:
    #         return 1
    #     elif column == 1 or column == 3:
    #         return 2
    #     return 3
    #
    # @staticmethod
    # def score_row_completion(game, move):
    #     if move.destination_type == DestinationType.FLOOR_LINE:
    #         return 0
    #
    #     if move.source_type == SourceType.FACTORY:
    #         tiles_taken = game.factories[move.source_index].tiles.count(move.tile)
    #     else:
    #         tiles_taken = game.centre.tiles.count(move.tile)
    #
    #     existing_tiles = game.current_player.pattern_lines[move.destination_index].count
    #     line_size = game.current_player.pattern_lines[move.destination_index].size
    #
    #     if existing_tiles + tiles_taken >= line_size:
    #         return 3
    #     return 0

    @staticmethod
    def check_row_completion(game, move):
        if move.destination_type == DestinationType.FLOOR_LINE:
            return False

        if move.source_type == SourceType.FACTORY:
            tiles_taken = game.factories[move.source_index].tiles.count(move.tile)
        else:
            tiles_taken = game.centre.tiles.count(move.tile)

        existing_tiles = game.current_player.pattern_lines[move.destination_index].count
        line_size = game.current_player.pattern_lines[move.destination_index].size

        if existing_tiles + tiles_taken >= line_size:
            return True
        return False

    @staticmethod
    def score_placement(game, move):
        if move.destination_type == DestinationType.FLOOR_LINE:
            return 0

        wall_clone = game.current_player.wall.clone()
        score, bonus =  wall_clone.place_tile(move.destination_index, move.tile)
        return score + bonus

    @staticmethod
    def score_penalty(game, move):
        existing_tiles = len(game.current_player.floor.tiles)
        existing_penalty = game.current_player.floor.points_lost()

        if move.source_type == SourceType.FACTORY:
            tiles_taken = game.factories[move.source_index].tiles.count(move.tile)
        else:
            tiles_taken = game.centre.tiles.count(move.tile)

        if move.destination_type == DestinationType.FLOOR_LINE:
            new_tiles = tiles_taken
        else:
            pattern_line_tiles = game.current_player.pattern_lines[move.destination_index].count
            line_size = game.current_player.pattern_lines[move.destination_index].size
            new_tiles = max(0, pattern_line_tiles + tiles_taken - line_size)

        if move.source_type == SourceType.CENTER and Tiles.STARTING in game.centre.tiles:
            new_tiles += 1

        total_tiles = existing_tiles + new_tiles

        new_penalty = 0
        for i in range(min(total_tiles, len(game.current_player.floor.PENALTIES))):
            new_penalty += game.current_player.floor.PENALTIES[i]

        return new_penalty - existing_penalty

    def score(self, game, move):
        score = 0
        if self.check_row_completion(game, move):
            score += self.score_placement(game, move)
        else:
            score += 1
        score -= self.score_penalty(game, move)
        return score

    def choose_move(self, game, moves, rng):
        if rng.random() < self.epsilon:
            return rng.choice(moves)

        scores = [self.score(game, move) for move in moves]
        best_score = max(scores)
        best_moves = [move for move, score in zip(moves, scores) if score == best_score]
        return rng.choice(best_moves)
