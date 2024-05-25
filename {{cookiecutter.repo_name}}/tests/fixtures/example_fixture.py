"""sample fixture."""

from uuid import uuid4

import pytest


@pytest.fixture(scope="session")
def test_session_id() -> str:
    return str(uuid4())[:6]
