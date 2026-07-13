"""Tests para el auditor de operaciones."""

import tempfile
from pathlib import Path
from stego_vault.core.audit_logger import AuditLogger


def test_log_and_read():
    with tempfile.TemporaryDirectory() as tmp:
        log_path = Path(tmp) / "test.jsonl"
        logger = AuditLogger(log_path)
        logger.log_analysis("test.png", "entropy", 2)
        entries = logger.read_all()
        assert len(entries) == 1
        assert entries[0]["event_type"] == "analysis_completed"


def test_log_multiple():
    with tempfile.TemporaryDirectory() as tmp:
        log_path = Path(tmp) / "test.jsonl"
        logger = AuditLogger(log_path)
        logger.log_analysis("test.png", "entropy", 2)
        logger.log_analysis("test.png", "lsb", 1)
        entries = logger.read_all()
        assert len(entries) == 2


def test_read_empty():
    with tempfile.TemporaryDirectory() as tmp:
        logger = AuditLogger(Path(tmp) / "empty.jsonl")
        assert logger.read_all() == []
