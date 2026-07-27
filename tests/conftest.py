import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import pytest  # noqa: E402

from innova_property_kit.model import PropertyBrief  # noqa: E402

BRIEF_PATH = ROOT / "briefs" / "via-petrarca-36.json"


@pytest.fixture
def petrarca() -> PropertyBrief:
    """Il brief di riferimento del progetto (Via F. Petrarca 36)."""
    return PropertyBrief.load(BRIEF_PATH).validate()
