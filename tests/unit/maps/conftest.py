from bokeh.plotting import Figure
from unittest.mock import MagicMock

import pytest


@pytest.fixture()
def mock_figure() -> MagicMock:
    return MagicMock(spec_set=Figure)
