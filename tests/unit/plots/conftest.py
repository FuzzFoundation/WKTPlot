from .common import PLOT_TITLE, STYLE_KWARGS
from unittest.mock import MagicMock
from wktplot.plots.standard import WKTPlot
from wktplot.plots.osm import OpenStreetMapsPlot

import tempfile
import pytest


@pytest.fixture()
def mock_bokeh(mocker) -> MagicMock:
    mock_bokeh: MagicMock = mocker.patch("wktplot.plots.standard.plt")
    return mock_bokeh


@pytest.fixture()
def temp_dir() -> str:
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# WKTPlot
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


@pytest.fixture()
def mock_plot(
    mock_bokeh: MagicMock,
    temp_dir: str,
) -> WKTPlot:

    plot = WKTPlot(
        title=PLOT_TITLE,
        save_dir=temp_dir,
        **STYLE_KWARGS,
    )
    plot.mapper = MagicMock()
    yield plot


@pytest.fixture()
def mock_plot_without_save_dir(
    mock_bokeh: MagicMock,
) -> WKTPlot:

    plot = WKTPlot(
        title=PLOT_TITLE,
        **STYLE_KWARGS,
    )
    plot.mapper = MagicMock()
    yield plot
