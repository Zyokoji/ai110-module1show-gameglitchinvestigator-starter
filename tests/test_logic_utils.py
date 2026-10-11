import pytest

from logic_utils import (
    check_guess,
    get_hint_message,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


# --- check_guess / get_hint_message (Bug 1) ---

def test_compares_numerically_not_as_text():
    # As strings, "9" > "50"; numerically 9 is lower.
    assert check_guess(9, 50) == "Too Low"
    assert check_guess(100, 9) == "Too High"


def test_string_secret_is_compared_as_number():
    assert check_guess(9, "50") == "Too Low"
    assert check_guess(50, "50") == "Win"


def test_too_high_hint_says_go_lower():
    assert "LOWER" in get_hint_message(check_guess(60, 50))


def test_too_low_hint_says_go_higher():
    assert "HIGHER" in get_hint_message(check_guess(40, 50))


def test_win_hint():
    assert "Correct" in get_hint_message(check_guess(50, 50))


# --- get_range_for_difficulty ---

@pytest.mark.parametrize(
    "difficulty, expected",
    [("Easy", (1, 20)), ("Normal", (1, 100)), ("Hard", (1, 50))],
)
def test_range_for_difficulty(difficulty, expected):
    assert get_range_for_difficulty(difficulty) == expected


# --- parse_guess ---

def test_parse_valid_guess():
    assert parse_guess("42") == (True, 42, None)


@pytest.mark.parametrize("raw", [None, ""])
def test_parse_empty_guess(raw):
    ok, value, err = parse_guess(raw)
    assert not ok and value is None and err == "Enter a guess."


def test_parse_non_number():
    ok, value, err = parse_guess("abc")
    assert not ok and value is None and err == "That is not a number."


# --- update_score ---

def test_first_attempt_win_scores_100():
    assert update_score(0, "Win", attempt_number=1) == 100


def test_win_points_drop_10_per_extra_attempt():
    assert update_score(0, "Win", attempt_number=2) == 90
    assert update_score(0, "Win", attempt_number=5) == 60


def test_win_points_have_minimum_of_10():
    assert update_score(0, "Win", attempt_number=10) == 10
    assert update_score(0, "Win", attempt_number=50) == 10


@pytest.mark.parametrize("attempt_number", [1, 2, 3, 4])
@pytest.mark.parametrize("outcome", ["Too High", "Too Low"])
def test_wrong_guess_always_costs_5(outcome, attempt_number):
    # Regression: "Too High" used to add 5 points on even attempts.
    assert update_score(50, outcome, attempt_number) == 45


@pytest.mark.parametrize("outcome", ["Too High", "Too Low"])
def test_score_never_goes_below_zero(outcome):
    assert update_score(0, outcome, attempt_number=1) == 0
    assert update_score(3, outcome, attempt_number=1) == 0


def test_unknown_outcome_leaves_score_unchanged():
    assert update_score(30, "Invalid", attempt_number=1) == 30


def test_winning_game_never_ends_negative():
    # Six wrong guesses then a win on attempt 7 (the scenario that produced -20).
    score = 0
    for attempt in range(1, 7):
        score = update_score(score, "Too Low", attempt)
    score = update_score(score, "Win", 7)
    assert score == 40
