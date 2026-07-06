"""Combat Regression Suite

Your task: write a thorough pytest test suite for rpg/combat.py.

Requirements (checked by check.py):
  - At least 2 @pytest.fixture definitions
  - At least 3 @pytest.mark.parametrize uses
  - At least 1 @pytest.mark.xfail test that detects the hidden bug in compute_damage
  - At least 85% coverage on rpg/combat.py

The hidden bug:
  compute_damage(atk=1, bonus=0, def_=10) returns 0 instead of 1.
  Write a test that asserts compute_damage(1, 0, 10) == 1 — it will fail.
  Mark it: @pytest.mark.xfail(reason="known bug: minimum damage should be 1, not 0")
  With xfail, pytest exits 0 even though the assertion fails.

Hints:
  - Use @pytest.fixture for Fighter objects you reuse across tests
  - Use @pytest.mark.parametrize to cover many (atk, bonus, def_, expected) cases at once
  - Test run_combat() with fighters where the outcome is predictable
  - Test compute_gold_reward() including edge cases and ValueError raises
"""

import pytest

# Import what you need:
# from rpg.combat import Fighter, apply_damage, compute_damage, compute_gold_reward, run_combat

# ── Write your fixtures and tests below ───────────────────────────────────────
