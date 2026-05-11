import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def db_path():
    with tempfile.TemporaryDirectory() as tmpdir:
        p = Path(tmpdir) / "test.db"
        os.environ["SRAPPLY_DB_PATH"] = str(p)
        yield str(p)


@pytest.fixture(scope="session")
def client(db_path):
    from app.services.database import close_db

    os.environ["SRAPPLY_DB_PATH"] = db_path
    close_db()

    from starlette.testclient import TestClient
    from app.main import app

    return TestClient(app)
