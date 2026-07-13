"""Tests para el gestor de scope."""

import tempfile
from pathlib import Path
from stego_vault.core.scope import ScopeManager


def test_default_scope():
    with tempfile.TemporaryDirectory() as tmp:
        scope = ScopeManager(Path(tmp) / "scope.json")
        assert not scope.is_authorized()


def test_set_authorized():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "scope.json"
        scope = ScopeManager(path)
        scope.set_authorized(True)
        scope.save()
        scope2 = ScopeManager(path)
        assert scope2.is_authorized()


def test_set_files():
    with tempfile.TemporaryDirectory() as tmp:
        scope = ScopeManager(Path(tmp) / "scope.json")
        scope.set_files(["test.png", "image.jpg"])
        assert scope.get_files() == ["test.png", "image.jpg"]


def test_require_authorization_raises():
    with tempfile.TemporaryDirectory() as tmp:
        scope = ScopeManager(Path(tmp) / "scope.json")
        try:
            scope.require_authorization()
            assert False
        except PermissionError:
            pass


def test_require_authorization_ok():
    with tempfile.TemporaryDirectory() as tmp:
        scope = ScopeManager(Path(tmp) / "scope.json")
        scope.set_authorized(True)
        scope.require_authorization()
