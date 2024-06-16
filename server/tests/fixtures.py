from __future__ import annotations

import pytest

from v2.utils.tests import LoggerAPIClient as APIClient


@pytest.fixture
def client() -> APIClient:
    return APIClient()
