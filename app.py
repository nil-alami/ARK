from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENDOR = ROOT / ".vendor"
if VENDOR.exists() and str(VENDOR) not in sys.path:
    sys.path.insert(0, str(VENDOR))

from ark_mvp.ui import CSS, build_app


if __name__ == "__main__":
    app = build_app()
    app.queue(default_concurrency_limit=1).launch(
        server_name=os.getenv("ARK_MVP_HOST", "127.0.0.1"),
        server_port=int(os.getenv("ARK_MVP_PORT", "7860")),
        show_error=True,
        inbrowser=False,
        css=CSS,
    )
