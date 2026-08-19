from __future__ import annotations

import sqlite3
import sys
import unittest
import uuid
from contextlib import closing
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / ".vendor"
if VENDOR.exists() and str(VENDOR) not in sys.path:
    sys.path.insert(0, str(VENDOR))

from ark_mvp.models import TraceStatus
from ark_mvp.pipeline import ExecutionPipeline
from ark_mvp.rendering import render_pipeline
from ark_mvp.sample_data import SCENARIO_INVALID, SCENARIO_SUCCESS
from ark_mvp.stages import STAGES
from ark_mvp.storage import SQLiteStore


class PipelineSmokeTests(unittest.TestCase):
    def setUp(self) -> None:
        data_dir = ROOT / ".data"
        data_dir.mkdir(exist_ok=True)
        self.db_path = data_dir / f"test-{uuid.uuid4().hex}.db"
        self.store = SQLiteStore(self.db_path)
        self.pipeline = ExecutionPipeline(self.store)

    def tearDown(self) -> None:
        for suffix in ("", "-shm", "-wal"):
            candidate = Path(f"{self.db_path}{suffix}")
            if candidate.exists():
                candidate.unlink()

    def test_complete_happy_path(self) -> None:
        snapshots = list(self.pipeline.execute(SCENARIO_SUCCESS))
        final = snapshots[-1]

        self.assertEqual("completed", final.status)
        self.assertEqual(216, final.input_rows)
        self.assertEqual(216, final.valid_rows)
        self.assertEqual(0, final.warning_count)
        self.assertEqual(72, len(final.recommendations))
        self.assertEqual(100, final.progress)

        latest = {event.stage_id: event for event in final.events}
        self.assertEqual({stage.stage_id for stage in STAGES}, set(latest))
        self.assertEqual(TraceStatus.QUEUED, latest["11-job"].status)
        self.assertTrue(
            all(
                event.status == TraceStatus.COMPLETED
                for stage_id, event in latest.items()
                if stage_id != "11-job"
            )
        )
        self.assertEqual(list(range(1, len(final.events) + 1)), [event.sequence for event in final.events])

        with closing(sqlite3.connect(self.db_path)) as connection:
            job_state, attempts = connection.execute(
                "SELECT state, attempt_count FROM jobs WHERE run_id = ?", (final.run_id,)
            ).fetchone()
            result_count = connection.execute(
                "SELECT COUNT(*) FROM results WHERE run_id = ?", (final.run_id,)
            ).fetchone()[0]
        self.assertEqual("succeeded", job_state)
        self.assertEqual(1, attempts)
        self.assertEqual(1, result_count)

    def test_invalid_rows_are_quarantined_and_valid_subset_runs(self) -> None:
        final = list(self.pipeline.execute(SCENARIO_INVALID))[-1]

        self.assertEqual("completed_with_warnings", final.status)
        self.assertEqual(220, final.input_rows)
        self.assertEqual(216, final.valid_rows)
        self.assertEqual(4, final.warning_count)
        self.assertEqual(72, len(final.recommendations))

        latest = {event.stage_id: event for event in final.events}
        self.assertEqual(TraceStatus.WARNING, latest["06-validation"].status)
        self.assertEqual(TraceStatus.WARNING, latest["07-quarantine"].status)
        self.assertIn("DEGRADED_CONTINUE", latest["07-quarantine"].branch_decision)

        with closing(sqlite3.connect(self.db_path)) as connection:
            quarantined = connection.execute(
                "SELECT COUNT(*) FROM quarantine_rows WHERE run_id = ?", (final.run_id,)
            ).fetchone()[0]
        self.assertEqual(4, quarantined)

    def test_rendered_pipeline_uses_latest_emitted_events(self) -> None:
        final = list(self.pipeline.execute(SCENARIO_SUCCESS))[-1]
        rendered = render_pipeline(final.events)
        for stage in STAGES:
            self.assertIn(escape(stage.stage_name), rendered)
        self.assertEqual(len(STAGES) - 1, rendered.count("pipeline-card completed"))
        self.assertEqual(1, rendered.count("pipeline-card queued"))


if __name__ == "__main__":
    unittest.main()
