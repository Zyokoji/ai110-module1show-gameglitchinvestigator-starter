# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

**Prompt used (Optional Challenge 1: Advanced Edge-Case Testing):**

```
I have completed the required Game Glitch Investigator project and now want to complete Optional Challenge 1: Advanced Edge-Case Testing. Review my existing code and pytest tests. Identify three meaningful edge cases not already covered, such as negative numbers, decimal inputs, and extremely large values. Add pytest cases verifying these inputs are handled gracefully without crashing or incorrectly updating the game state. Preserve all existing behavior and tests. Run the full pytest suite and report the actual results. Update ai_interactions.md with my prompt and a one-line explanation for each edge case. Do not modify README.md yet.
```

Tests are in `tests/test_edge_cases.py`.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Negative numbers (`-5`, `-0`, `-100`) | Challenge 1 prompt above | `test_negative_input_parses_to_negative_int`, `test_negative_guess_is_too_low_and_hints_higher`, `test_negative_guess_in_app_does_not_crash_or_end_game` | Yes | A negative guess is a valid number below every secret, so it should be parsed, called "Too Low" with a "Go HIGHER" hint, and never push the score below 0. |
| Decimal inputs (`42.9`, `.5`, `-2.5`, `4.2.1`) | Challenge 1 prompt above | `test_decimal_input_truncates_toward_zero`, `test_malformed_decimal_is_rejected`, `test_decimal_that_truncates_to_secret_wins`, `test_malformed_decimal_in_app_leaves_score_and_status_unchanged` | Yes | Decimals are truncated toward zero (not rounded), and malformed decimals are rejected with an error instead of crashing or changing the score. |
| Extremely large values (30-digit int, `1e400`, `1.5e400`, `inf`, `nan`, 5000 digits) | Challenge 1 prompt above | `test_huge_integer_parses_and_compares_without_overflow`, `test_overflowing_or_non_finite_input_is_rejected`, `test_rejected_input_never_changes_score`, `test_huge_value_in_app_does_not_crash_or_change_score` | Yes | Python ints never overflow, but `int(float("1.5e400"))` raises `OverflowError` and 5000-digit strings exceed Python's digit limit, so these must be caught and reported as "not a number". |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
