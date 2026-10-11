"""Edge-case tests: negative numbers, decimal inputs, and extremely large values."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from logic_utils import check_guess, get_hint_message, parse_guess, update_score

APP_PATH = str(Path(__file__).resolve().parent.parent / "app.py")


def play_one_guess(raw, secret=50):
    """Run the real app, submit one raw guess, and return the AppTest after the rerun."""
    at = AppTest.from_file(APP_PATH).run()
    at.session_state.secret = secret
    at.text_input[0].input(raw)
    at.button[0].click().run()
    return at


# --- Edge case 1: negative numbers ---

@pytest.mark.parametrize("raw, expected", [("-5", -5), ("-0", 0), ("-100", -100)])
def test_negative_input_parses_to_negative_int(raw, expected):
    assert parse_guess(raw) == (True, expected, None)


def test_negative_guess_is_too_low_and_hints_higher():
    outcome = check_guess(-5, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in get_hint_message(outcome)


def test_negative_guess_in_app_does_not_crash_or_end_game():
    at = play_one_guess("-5")
    assert not at.exception
    assert at.session_state.status == "playing"
    assert at.session_state.score == 0  # wrong-guess penalty is floored at 0
    assert at.session_state.history == [-5]


# --- Edge case 2: decimal inputs ---

@pytest.mark.parametrize(
    "raw, expected",
    [("42.9", 42), ("42.0", 42), (".5", 0), ("-2.5", -2)],
)
def test_decimal_input_truncates_toward_zero(raw, expected):
    assert parse_guess(raw) == (True, expected, None)


@pytest.mark.parametrize("raw", ["4.2.1", ".", "3..5"])
def test_malformed_decimal_is_rejected(raw):
    assert parse_guess(raw) == (False, None, "That is not a number.")


def test_decimal_that_truncates_to_secret_wins():
    ok, value, _ = parse_guess("50.7")
    assert ok and check_guess(value, 50) == "Win"


def test_malformed_decimal_in_app_leaves_score_and_status_unchanged():
    at = play_one_guess("4.2.1")
    assert not at.exception
    assert any("not a number" in e.value for e in at.error)
    assert at.session_state.status == "playing"
    assert at.session_state.score == 0
    assert at.session_state.secret == 50


# --- Edge case 3: extremely large values ---

def test_huge_integer_parses_and_compares_without_overflow():
    huge = "9" * 30
    ok, value, err = parse_guess(huge)
    assert ok and value == int(huge) and err is None
    assert check_guess(value, 50) == "Too High"


@pytest.mark.parametrize(
    "raw",
    [
        "1e400",      # scientific notation without a dot is not an int literal
        "1.5e400",    # float() gives inf, and int(inf) raises OverflowError
        "inf",
        "nan",
        # Longer than Python's int-string digit limit.
        pytest.param("1" * 5000, id="5000-digits"),
    ],
)
def test_overflowing_or_non_finite_input_is_rejected(raw):
    assert parse_guess(raw) == (False, None, "That is not a number.")


def test_rejected_input_never_changes_score():
    # app.py only calls update_score for parsed guesses; nothing else should move the score.
    ok, _, _ = parse_guess("1.5e400")
    assert not ok
    assert update_score(40, "Invalid", attempt_number=3) == 40


def test_huge_value_in_app_does_not_crash_or_change_score():
    at = play_one_guess("1.5e400")
    assert not at.exception
    assert any("not a number" in e.value for e in at.error)
    assert at.session_state.status == "playing"
    assert at.session_state.score == 0
    assert at.session_state.secret == 50
