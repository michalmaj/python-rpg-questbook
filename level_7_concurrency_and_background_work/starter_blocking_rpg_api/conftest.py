import sys
from pathlib import Path

# When running pytest from the repo root, insert this starter's directory at
# the front of sys.path so that "rpg.*" imports resolve here, not to the L4
# installable CLI package that the root pyproject.toml puts on the path first.
sys.path.insert(0, str(Path(__file__).parent))
