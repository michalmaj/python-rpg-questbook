"""Author-only provenance tool for the Final Analytics Epilogue fixtures.

Students never need to run this. It regenerates the four fixture files in
../data/ by calling the REAL, frozen Level 7 Project 03 domain/service code
(rpg.domain, rpg.services, rpg.repositories from
level_7_concurrency_and_background_work/projects/03_concurrent_tournament_runner)
— it does not reimplement any combat rule. The only "generation logic" here
is orchestration: which hero class fights which monster, how many runs/
battles, and writing the resulting BattleResult data to JSON/CSV.

Reproducibility: BattleService.simulate() (and the rest of rpg.services)
calls the stdlib `random` module's *global* functions directly (e.g.
`random.randint(1, 6)`), not an injected Random instance. Verified
empirically (see the epilogue's final report) that seeding the global
module with `random.seed(n)` before a sequence of simulate() calls makes
that sequence exactly reproducible, with no changes to the frozen L7 code.
This script seeds once per fixture, right before that fixture's first
simulate() call, then calls simulate() in a fixed, deterministic order.

Run twice from a clean state; all four output files must be byte-for-byte
identical both times (verified separately, not by this script).
"""
import csv
import json
import random
import sys
from pathlib import Path

EPILOGUE_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = EPILOGUE_ROOT.parent
L7_P03_ROOT = REPO_ROOT / "level_7_concurrency_and_background_work" / "projects" / "03_concurrent_tournament_runner"
DATA_DIR = EPILOGUE_ROOT / "data"

sys.path.insert(0, str(L7_P03_ROOT))
from rpg.domain import HeroClass  # noqa: E402
from rpg.repositories import MonsterRepository  # noqa: E402
from rpg.services import BattleService, create_hero  # noqa: E402

_repo = MonsterRepository(L7_P03_ROOT / "data" / "monsters.json")
_service = BattleService(_repo)

# ── Fixture A: Deep Dive — ~500 battles of one fixed matchup ───────────────

DEEP_DIVE_PRIMARY = {"hero_class": HeroClass.warrior, "monster": "Goblin", "seed": 20240501, "n": 500}
DEEP_DIVE_VARIANT = {"hero_class": HeroClass.rogue, "monster": "Goblin", "seed": 20240502, "n": 500}


def generate_deep_dive(hero_class: HeroClass, monster: str, seed: int, n: int) -> dict:
    random.seed(seed)
    hero = create_hero("Deep Dive Hero", hero_class)
    battles = []
    for _ in range(n):
        result = _service.simulate(hero, monster)
        battles.append({
            "winner": result.winner,
            "rounds": result.rounds,
            "gold_earned": result.gold_earned,
        })
    return {
        "hero_class": hero_class.value,
        "monster": monster,
        "matchup": f"{hero_class.value}_vs_{monster}",
        "battles": battles,
    }


# ── Fixture B: Tournament History — many runs across every matchup ────────

BATTLES_PER_RUN = 30

# Primary: uniform 5 runs per matchup (3 classes x 3 monsters x 5 = 45 runs).
HISTORY_PRIMARY_RUN_COUNTS = {
    (HeroClass.warrior, "Goblin"): 5, (HeroClass.warrior, "Orc"): 5, (HeroClass.warrior, "Dragon"): 5,
    (HeroClass.mage, "Goblin"): 5, (HeroClass.mage, "Orc"): 5, (HeroClass.mage, "Dragon"): 5,
    (HeroClass.rogue, "Goblin"): 5, (HeroClass.rogue, "Orc"): 5, (HeroClass.rogue, "Dragon"): 5,
}
HISTORY_PRIMARY_SEED = 310120

# Variant: same 9 matchups, same total run count (45), but a different
# tournament organizer chose to run more battles against the matchups they
# were curious about — a deliberately different, still-45-run allocation.
# (Every individual matchup's win/loss outcome in this frozen domain is
# fully determined by hero-class-vs-monster stats, not by how many runs are
# spent on it — confirmed empirically, see final report — so this is the
# legitimate lever for making the tournament's aggregate conclusions differ
# between primary and variant without fabricating any battle outcome.)
HISTORY_VARIANT_RUN_COUNTS = {
    (HeroClass.warrior, "Goblin"): 3, (HeroClass.warrior, "Orc"): 3, (HeroClass.warrior, "Dragon"): 9,
    (HeroClass.mage, "Goblin"): 7, (HeroClass.mage, "Orc"): 7, (HeroClass.mage, "Dragon"): 1,
    (HeroClass.rogue, "Goblin"): 5, (HeroClass.rogue, "Orc"): 5, (HeroClass.rogue, "Dragon"): 5,
}
HISTORY_VARIANT_SEED = 310121


def generate_history(run_counts: dict, seed: int, battles_per_run: int) -> list[dict]:
    random.seed(seed)
    rows = []
    run_id = 1
    # Fixed, deterministic iteration order: HeroClass enum order, then a
    # fixed monster order — not dict insertion order, which could vary.
    monster_order = ["Goblin", "Orc", "Dragon"]
    for hero_class in HeroClass:
        hero = create_hero("Tournament Hero", hero_class)
        for monster in monster_order:
            n_runs = run_counts[(hero_class, monster)]
            for _ in range(n_runs):
                hero_wins = 0
                rounds_total = 0
                gold_total = 0
                for _ in range(battles_per_run):
                    result = _service.simulate(hero, monster)
                    rounds_total += result.rounds
                    gold_total += result.gold_earned
                    if result.winner == "hero":
                        hero_wins += 1
                rows.append({
                    "run_id": run_id,
                    "hero_class": hero_class.value,
                    "monster": monster,
                    "matchup": f"{hero_class.value}_vs_{monster}",
                    "battles": battles_per_run,
                    "hero_wins": hero_wins,
                    "hero_win_rate": round(hero_wins / battles_per_run, 6),
                    "avg_rounds": round(rounds_total / battles_per_run, 6),
                    "avg_gold": round(gold_total / battles_per_run, 6),
                })
                run_id += 1
    return rows


HISTORY_FIELDNAMES = [
    "run_id", "hero_class", "monster", "matchup", "battles",
    "hero_wins", "hero_win_rate", "avg_rounds", "avg_gold",
]


def write_deep_dive(data: dict, path: Path) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n")


def write_history(rows: list[dict], path: Path) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HISTORY_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    primary_deep_dive = generate_deep_dive(**DEEP_DIVE_PRIMARY)
    variant_deep_dive = generate_deep_dive(**DEEP_DIVE_VARIANT)
    write_deep_dive(primary_deep_dive, DATA_DIR / "deep_dive_battles.json")
    write_deep_dive(variant_deep_dive, DATA_DIR / "deep_dive_battles_variant.json")

    primary_history = generate_history(HISTORY_PRIMARY_RUN_COUNTS, HISTORY_PRIMARY_SEED, BATTLES_PER_RUN)
    variant_history = generate_history(HISTORY_VARIANT_RUN_COUNTS, HISTORY_VARIANT_SEED, BATTLES_PER_RUN)
    write_history(primary_history, DATA_DIR / "tournament_history.csv")
    write_history(variant_history, DATA_DIR / "tournament_history_variant.csv")

    print(f"Wrote {len(primary_deep_dive['battles'])} primary deep-dive battles "
          f"({primary_deep_dive['matchup']})")
    print(f"Wrote {len(variant_deep_dive['battles'])} variant deep-dive battles "
          f"({variant_deep_dive['matchup']})")
    print(f"Wrote {len(primary_history)} primary history runs")
    print(f"Wrote {len(variant_history)} variant history runs")


if __name__ == "__main__":
    main()
