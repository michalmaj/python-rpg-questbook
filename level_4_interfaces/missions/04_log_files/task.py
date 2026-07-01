"""
Mission 04: Log Files

M03 taught logging to the console. Events disappear when the process exits.
This mission adds FileHandlers so logs are written to disk and persist.

Your task:
1. Implement add_file_handler() — adds a FileHandler to any logger
2. Implement setup_log_files() — wires up app.log and combat.log
3. Replace # USE combat_logger markers with combat_logger.* calls
"""

import csv
import json
import logging
import random
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError

# ----- loggers ----------------------------------------------------------------

logger = logging.getLogger(__name__)
combat_logger = logging.getLogger(__name__ + ".combat")

# ----- paths ------------------------------------------------------------------

_ROOT = Path(__file__).parent
DATA_DIR = _ROOT / "data"
SAVES_DIR = _ROOT / "saves"
LOG_DIR = _ROOT / "logs"
SAVE_FILE = SAVES_DIR / "save_game.json"
LOG_FILE = SAVES_DIR / "combat_log.csv"

CURRENT_SCHEMA_VERSION = 1


# ----- domain -----------------------------------------------------------------


class HeroClass(Enum):
    WARRIOR = "warrior"
    MAGE = "mage"
    ROGUE = "rogue"


@dataclass
class Hero:
    name: str
    hero_class: HeroClass
    hp: int
    max_hp: int
    atk: int
    def_: int
    potions: int = 3
    gold: int = 0
    wins: int = 0
    losses: int = 0

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)

    def use_potion(self) -> bool:
        if self.potions <= 0:
            return False
        self.hp = min(self.hp + 30, self.max_hp)
        self.potions -= 1
        return True


@dataclass
class Monster:
    name: str
    hp: int
    atk: int
    def_: int
    gold: int

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)


# ----- Pydantic models --------------------------------------------------------


class MonsterConfig(BaseModel):
    name: str
    hp: int = Field(gt=0)
    atk: int = Field(ge=1)
    def_: int = Field(ge=0, alias="def")
    gold: int = Field(ge=0)

    model_config = {"populate_by_name": True}

    def to_domain(self) -> Monster:
        return Monster(name=self.name, hp=self.hp, atk=self.atk,
                       def_=self.def_, gold=self.gold)


class SaveGameModel(BaseModel):
    schema_version: int = Field(default=CURRENT_SCHEMA_VERSION, ge=1)
    name: str
    hero_class: str
    hp: int = Field(ge=0)
    max_hp: int = Field(gt=0)
    atk: int = Field(ge=1)
    def_: int = Field(ge=0)
    potions: int = Field(ge=0)
    gold: int = Field(ge=0)
    wins: int = Field(ge=0)
    losses: int = Field(ge=0)

    def to_hero(self) -> Hero:
        return Hero(
            name=self.name, hero_class=HeroClass(self.hero_class),
            hp=self.hp, max_hp=self.max_hp, atk=self.atk, def_=self.def_,
            potions=self.potions, gold=self.gold, wins=self.wins, losses=self.losses,
        )

    @classmethod
    def from_hero(cls, hero: Hero) -> "SaveGameModel":
        return cls(
            name=hero.name, hero_class=hero.hero_class.value,
            hp=hero.hp, max_hp=hero.max_hp, atk=hero.atk, def_=hero.def_,
            potions=hero.potions, gold=hero.gold, wins=hero.wins, losses=hero.losses,
        )


# ----- your work: logging setup ----------------------------------------------

DEFAULT_FMT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"


def setup_logging(level: str = "INFO") -> None:
    """Configure the root logger with a StreamHandler."""
    log_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(level=log_level, format=DEFAULT_FMT)


def add_file_handler(
    target_logger: logging.Logger,
    path: Path,
    level: int = logging.INFO,
    fmt: str = DEFAULT_FMT,
) -> None:
    # TODO:
    # 1. Create parent directories: path.parent.mkdir(parents=True, exist_ok=True)
    # 2. Create logging.FileHandler(path, encoding="utf-8")
    # 3. handler.setLevel(level)
    # 4. handler.setFormatter(logging.Formatter(fmt))
    # 5. target_logger.addHandler(handler)
    raise NotImplementedError


def setup_log_files(log_dir: Path = LOG_DIR) -> None:
    # TODO:
    # 1. Add app.log to the ROOT logger at INFO level:
    #    add_file_handler(logging.getLogger(), log_dir / "app.log", logging.INFO)
    # 2. Add combat.log to the combat logger at DEBUG level:
    #    add_file_handler(combat_logger, log_dir / "combat.log", logging.DEBUG)
    raise NotImplementedError


# ----- data loading -----------------------------------------------------------


def load_monsters() -> list[Monster]:
    try:
        with open(DATA_DIR / "monsters.json") as f:
            raw = json.load(f)
        monsters = []
        for entry in raw["monsters"]:
            try:
                config = MonsterConfig.model_validate(entry)
                monsters.append(config.to_domain())
            except ValidationError as e:
                logger.warning("Skipped bad monster entry: %s", e)
        return monsters
    except Exception:
        logger.exception("Error loading monsters")
        return []


def load_hero_classes() -> dict:
    try:
        with open(DATA_DIR / "hero_classes.json") as f:
            return json.load(f)
    except Exception:
        logger.exception("Error loading hero classes")
        return {}


# ----- persistence ------------------------------------------------------------


def save_game(hero: Hero) -> None:
    SAVES_DIR.mkdir(exist_ok=True)
    model = SaveGameModel.from_hero(hero)
    SAVE_FILE.write_text(model.model_dump_json(indent=2))
    logger.info("Game saved for %s", hero.name)
    print("Game saved.")


def load_game() -> Hero | None:
    if not SAVE_FILE.exists():
        logger.debug("No save file found at %s", SAVE_FILE)
        return None
    try:
        model = SaveGameModel.model_validate_json(SAVE_FILE.read_text())
        if model.schema_version != CURRENT_SCHEMA_VERSION:
            logger.warning(
                "Save version %d != %d, starting fresh",
                model.schema_version, CURRENT_SCHEMA_VERSION,
            )
            return None
        logger.info("Loaded hero: %s (%s)", model.name, model.hero_class)
        return model.to_hero()
    except (ValidationError, ValueError):
        logger.exception("Could not load save")
        return None


# ----- combat logging ---------------------------------------------------------


def _append_log_row(
    battle_id: int, turn: int, hero: Hero, monster: Monster,
    action: str, damage_dealt: int, damage_taken: int, result: str,
) -> None:
    SAVES_DIR.mkdir(exist_ok=True)
    write_header = not LOG_FILE.exists()
    with LOG_FILE.open("a", newline="") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(["battle_id", "turn", "hero_name", "hero_class", "monster",
                         "action", "damage_dealt", "damage_taken", "hero_hp", "monster_hp", "result"])
        w.writerow([battle_id, turn, hero.name, hero.hero_class.value, monster.name,
                    action, damage_dealt, damage_taken, hero.hp, monster.hp, result])
    # USE combat_logger (replace this print with combat_logger.debug)
    print(f"[combat] turn {turn} battle {battle_id}: {action} {result}")


# ----- pure logic -------------------------------------------------------------


def compute_damage(atk: int, def_: int, dice_roll: int) -> int:
    return max(1, atk + dice_roll - def_)


# ----- hero creation ----------------------------------------------------------


def choose_hero() -> Hero:
    classes = load_hero_classes()
    name = input("Hero name: ").strip() or "Hero"

    print("\nChoose class:")
    keys = list(classes.keys())
    for i, key in enumerate(keys, 1):
        d = classes[key]
        print(f"  {i}. {key.title()} — {d['description']}")

    choice = input("Choice (1-3): ").strip()
    try:
        idx = int(choice) - 1
        if not 0 <= idx < len(keys):
            raise ValueError
        chosen = keys[idx]
    except ValueError:
        logger.warning("Invalid class choice '%s', defaulting to warrior", choice)
        chosen = "warrior"

    d = classes[chosen]
    return Hero(
        name=name, hero_class=HeroClass(chosen),
        hp=d["hp"], max_hp=d["hp"], atk=d["atk"], def_=d["def"],
    )


# ----- combat loop ------------------------------------------------------------


def run_combat(hero: Hero, monster: Monster, battle_id: int) -> bool:
    # USE combat_logger (replace this print with combat_logger.info)
    print(f"[combat] start — {hero.name} vs {monster.name}, battle #{battle_id}")
    print(f"\n⚔  {hero.name} vs {monster.name}!")
    turn = 1

    while hero.is_alive and monster.is_alive:
        print(
            f"\nTurn {turn} | "
            f"{hero.name} HP: {hero.hp}/{hero.max_hp} | "
            f"{monster.name} HP: {monster.hp}"
        )
        action = input("Action — [a]ttack / [p]otion: ").strip().lower()

        if action == "p":
            if hero.use_potion():
                print(f"  Used potion. HP restored to {hero.hp}.")
                _append_log_row(battle_id, turn, hero, monster, "potion", 0, 0, "ongoing")
            else:
                print("  No potions left!")
            turn += 1
            continue

        dice = random.randint(1, 6)
        dmg = compute_damage(hero.atk, monster.def_, dice)
        monster.take_damage(dmg)
        # USE combat_logger (replace this print with combat_logger.debug)
        print(f"[combat] hero attacks for {dmg} (dice={dice})")
        print(f"  You deal {dmg} damage (rolled {dice}). Monster HP: {monster.hp}")

        if not monster.is_alive:
            _append_log_row(battle_id, turn, hero, monster, "attack", dmg, 0, "win")
            print(f"\n✅ Victory! +{monster.gold} gold.")
            hero.gold += monster.gold
            hero.wins += 1
            return True

        mdice = random.randint(1, 6)
        mdmg = compute_damage(monster.atk, hero.def_, mdice)
        hero.take_damage(mdmg)
        # USE combat_logger (replace this print with combat_logger.debug)
        print(f"[combat] monster attacks for {mdmg} (dice={mdice})")
        print(f"  {monster.name} deals {mdmg} damage. Your HP: {hero.hp}")

        result = "ongoing" if hero.is_alive else "loss"
        _append_log_row(battle_id, turn, hero, monster, "attack", dmg, mdmg, result)

        if not hero.is_alive:
            print("\n💀 You were defeated.")
            hero.losses += 1
            return False

        turn += 1

    return hero.is_alive


# ----- main -------------------------------------------------------------------


def main() -> None:
    import os
    level = os.environ.get("RPG_LOG_LEVEL", "INFO")
    setup_logging(level)

    try:
        setup_log_files()
    except NotImplementedError:
        print("TODO: implement setup_log_files() first.")
        return

    logger.info("RPG Dungeon starting")
    print("=== RPG Dungeon ===\n")

    existing = load_game()
    if existing:
        ans = input(f"Continue as {existing.name}? [y/n]: ").strip().lower()
        hero = existing if ans == "y" else choose_hero()
    else:
        hero = choose_hero()

    monsters = load_monsters()
    if not monsters:
        logger.error("No monsters loaded")
        print("No monsters loaded. Check data/monsters.json.")
        sys.exit(1)

    battle_id = 1
    while True:
        print(
            f"\n--- {hero.name} | HP: {hero.hp}/{hero.max_hp} | "
            f"Gold: {hero.gold} | Potions: {hero.potions} ---"
        )
        print("  [f] Fight   [s] Save   [q] Quit")
        cmd = input("> ").strip().lower()

        if cmd == "f":
            monster = random.choice(monsters)
            run_combat(hero, monster, battle_id)
            battle_id += 1
        elif cmd == "s":
            save_game(hero)
        elif cmd == "q":
            save_game(hero)
            logger.info("Session ended for %s", hero.name)
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
