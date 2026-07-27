#!/usr/bin/env python3
"""Entry point del kit: `python innova_property_kit.py --help`.

Sottile wrapper attorno a `tools/innova_property_kit`, cosi lo strumento si lancia
dalla radice del repository senza installare nulla.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "tools"))

from innova_property_kit.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
