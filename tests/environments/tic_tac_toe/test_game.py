import pytest
from environments.tic_tac_toe.game import Game, Marker

WINNING_COMBINATIONS = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]

DRAW_BOARD = [
    Marker.X, Marker.O, Marker.X,
    Marker.X, Marker.O, Marker.O,
    Marker.O, Marker.X, Marker.X,
]


def snapshot(game):
    return game.board.copy(), game.current_player


def test_marker_values_and_score_bounds():
    assert Marker.X.value == "X"
    assert Marker.O.value == "O"
    assert Marker.EMPTY.value == " "
    assert Game.max_possible_score == 1
    assert Game.min_possible_score == -1


def test_initial_state():
    game = Game()

    assert game.player_one is Marker.X
    assert game.player_two is Marker.O
    assert game.current_player is Marker.X
    assert game.board == [Marker.EMPTY] * 9


def test_game_instances_do_not_share_board_state():
    first_game = Game()
    second_game = Game()

    first_game.board[0] = Marker.X

    assert first_game.board is not second_game.board
    assert second_game.board == [Marker.EMPTY] * 9


def test_chance_node_is_not_required():
    assert Game.chance_node_required() is False
    assert Game().chance_node_required() is False


def test_all_positions_are_initially_legal_in_ascending_order():
    assert Game().get_legal_actions() == list(range(9))


def test_occupied_positions_are_excluded_from_legal_actions():
    game = Game()
    game.make_move(0)
    game.make_move(4)

    assert game.get_legal_actions() == [1, 2, 3, 5, 6, 7, 8]


def test_make_move_places_marker_switches_player_and_returns_true():
    game = Game()

    result = game.make_move(3)

    assert result is True
    assert game.board[3] is Marker.X
    assert game.current_player is Marker.O


def test_successive_moves_alternate_markers():
    game = Game()

    game.make_move(0)
    game.make_move(1)
    game.make_move(2)

    assert game.board[:3] == [Marker.X, Marker.O, Marker.X]
    assert game.current_player is Marker.O


def test_make_move_accepts_integer_string():
    game = Game()

    game.make_move("4")

    assert game.board[4] is Marker.X
    assert game.current_player is Marker.O


def test_apply_deterministic_move_matches_make_move():
    deterministic_game = Game()
    regular_game = Game()

    deterministic_result = deterministic_game.apply_deterministic_move(5)
    regular_result = regular_game.make_move(5)

    assert deterministic_result is regular_result is True
    assert deterministic_game.board == regular_game.board
    assert deterministic_game.current_player is regular_game.current_player


@pytest.mark.parametrize(
    "position",
    [
        pytest.param(None, id="none"),
        pytest.param("one", id="non-numeric-string"),
        pytest.param(1.0, id="integral-float"),
        pytest.param(1.5, id="fractional-float"),
        pytest.param(True, id="true"),
        pytest.param(False, id="false"),
        pytest.param([], id="list"),
    ],
)
def test_make_move_rejects_invalid_types_without_changing_state(position):
    game = Game()
    original_state = snapshot(game)

    with pytest.raises(ValueError, match=r"^Invalid move\. Position must be an integer\.$"):
        game.make_move(position)

    assert snapshot(game) == original_state


@pytest.mark.parametrize("position", [-1, 9, "9"])
def test_make_move_rejects_out_of_bounds_position_without_changing_state(position):
    game = Game()
    original_state = snapshot(game)

    with pytest.raises(
        ValueError,
        match=r"^Invalid move\. Position is either occupied or out of bounds\.$",
    ):
        game.make_move(position)

    assert snapshot(game) == original_state


def test_make_move_rejects_occupied_position_without_changing_state():
    game = Game()
    game.make_move(2)
    original_state = snapshot(game)

    with pytest.raises(
        ValueError,
        match=r"^Invalid move\. Position is either occupied or out of bounds\.$",
    ):
        game.make_move(2)

    assert snapshot(game) == original_state


@pytest.mark.parametrize(
    "board",
    [
        pytest.param(
            [Marker.X, Marker.X, Marker.X] + [Marker.EMPTY] * 6,
            id="victory",
        ),
        pytest.param(DRAW_BOARD, id="draw"),
    ],
)
def test_make_move_rejects_moves_after_game_ends_without_changing_state(board):
    game = Game()
    game.board = board.copy()
    original_state = snapshot(game)

    with pytest.raises(
        ValueError,
        match=r"^Game has already ended\. No more moves can be made\.$",
    ):
        game.make_move(0)

    assert snapshot(game) == original_state


@pytest.mark.parametrize("combination", WINNING_COMBINATIONS)
@pytest.mark.parametrize("marker", [Marker.X, Marker.O])
def test_check_victory_detects_every_winning_combination(combination, marker):
    game = Game()
    for position in combination:
        game.board[position] = marker

    assert game.check_victory() == marker.value


@pytest.mark.parametrize(
    "board",
    [
        pytest.param([Marker.EMPTY] * 9, id="empty"),
        pytest.param(
            [
                Marker.X, Marker.O, Marker.X,
                Marker.EMPTY, Marker.O, Marker.EMPTY,
                Marker.EMPTY, Marker.X, Marker.EMPTY,
            ],
            id="partial",
        ),
        pytest.param(DRAW_BOARD, id="full-draw"),
    ],
)
def test_check_victory_returns_none_without_winner(board):
    game = Game()
    game.board = board.copy()

    assert game.check_victory() is None


def test_check_end_is_false_for_ongoing_game():
    game = Game()
    game.make_move(0)
    game.make_move(4)

    assert game.check_end() is False


def test_check_end_is_true_for_victory_with_empty_positions():
    game = Game()
    game.board = [Marker.X, Marker.X, Marker.X] + [Marker.EMPTY] * 6

    assert game.get_legal_actions()
    assert game.check_end() is True


def test_full_non_winning_board_is_a_terminal_draw():
    game = Game()
    game.board = DRAW_BOARD.copy()

    assert game.get_legal_actions() == []
    assert game.check_victory() is None
    assert game.check_end() is True


def test_clone_preserves_state_without_sharing_mutable_board():
    game = Game()
    game.make_move(0)
    game.make_move(4)

    cloned_game = game.clone()

    assert cloned_game is not game
    assert cloned_game.board == game.board
    assert cloned_game.board is not game.board
    assert cloned_game.player_one is game.player_one
    assert cloned_game.player_two is game.player_two
    assert cloned_game.current_player is game.current_player

    cloned_game.make_move(1)
    assert game.board[1] is Marker.EMPTY

    game.make_move(2)
    assert cloned_game.board[2] is Marker.EMPTY


def test_display_game_renders_board_exactly():
    game = Game()
    game.board = [
        Marker.X, Marker.O, Marker.EMPTY,
        Marker.EMPTY, Marker.X, Marker.O,
        Marker.O, Marker.EMPTY, Marker.X,
    ]

    assert game.display_game() == (
        "X | O |  \n"
        "---------\n"
        "  | X | O\n"
        "---------\n"
        "O |   | X\n"
    )
