"""
Mission 07: Settings and Paths

The starter RPG has paths scattered as module-level variables:

    DATA_DIR = "level_3_validation_and_persistence/starter_raw_rpg/data"
    SAVES_DIR = "level_3_validation_and_persistence/starter_raw_rpg/saves"
    LOG_PATH  = "level_3_validation_and_persistence/starter_raw_rpg/saves/combat_log.csv"

Problems:
  - Hardcoded strings — no type checking, no validation
  - No single source of truth — each module defines its own paths
  - Running the game from a different directory breaks everything
  - Impossible to override paths without editing source code

Your task: define GameSettings using Pydantic BaseSettings (or plain BaseModel)
so all paths live in one validated object that can be overridden via environment
variables or a .env file.
"""

from pathlib import Path

# from pydantic import Field
# from pydantic_settings import BaseSettings, SettingsConfigDict

_REPO_ROOT = Path(__file__).parents[3]
_LEVEL3_ROOT = _REPO_ROOT / "level_3_validation_and_persistence"


# ---------------------------------------------------------------------------
# TODO: Define GameSettings using BaseSettings from pydantic-settings
#
# Values can be overridden via environment variables
# (e.g. export RPG_SAVES_DIR=/tmp/test_saves).
#
# Required fields (with defaults):
#   data_dir   : Path = _LEVEL3_ROOT / "starter_raw_rpg" / "data"
#   saves_dir  : Path = _LEVEL3_ROOT / "starter_raw_rpg" / "saves"
#   log_file   : Path = _LEVEL3_ROOT / "starter_raw_rpg" / "saves" / "combat_log.csv"
#   max_potions: int  = 5
#
# Add a model_config that:
#   - reads from a .env file called ".env" in the current directory
#   - uses env_prefix="RPG_" so the env var for data_dir is RPG_DATA_DIR
#
# Example:
#   class GameSettings(BaseSettings):
#       model_config = SettingsConfigDict(env_prefix="RPG_", env_file=".env")
#       data_dir: Path = _LEVEL3_ROOT / "starter_raw_rpg" / "data"
#       ...
# ---------------------------------------------------------------------------

# class GameSettings(BaseSettings):
#     ...


# ---------------------------------------------------------------------------
# TODO: Define get_settings() → GameSettings
#
# Return a cached GameSettings instance.
# Pattern:
#
#   _settings: GameSettings | None = None
#
#   def get_settings() -> GameSettings:
#       global _settings
#       if _settings is None:
#           _settings = GameSettings()
#       return _settings
#
# This is the simplest form of dependency injection:
# everywhere in the game that needs paths calls get_settings() instead
# of importing a global variable.
# ---------------------------------------------------------------------------

# def get_settings() -> GameSettings:
#     ...


# ---------------------------------------------------------------------------
# runner
# ---------------------------------------------------------------------------


def main() -> None:
    # settings = get_settings()
    # print(f"data_dir  : {settings.data_dir}")
    # print(f"saves_dir : {settings.saves_dir}")
    # print(f"log_file  : {settings.log_file}")
    # print(f"max_potions: {settings.max_potions}")
    # print(f"\ndata_dir exists: {settings.data_dir.exists()}")
    pass


if __name__ == "__main__":
    main()
