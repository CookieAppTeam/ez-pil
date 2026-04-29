import sys
from pathlib import Path

# Add root to make ez_pil import work
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
