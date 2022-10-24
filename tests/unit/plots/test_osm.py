from .common import PLOT_TITLE, STYLE_KWARGS
from bokeh.tile_providers import Vendors
from pytest_mock import MockFixture
from unittest.mock import MagicMock
from wktplot.plots.osm import OpenStreetMapsPlot


class TestConstructor:

    def test_when_given_valid_arguments_figure_class_var_set(
        self,
        mocker: MockFixture,
        temp_dir: str,
        mock_bokeh: MagicMock,
    ) -> None:

        mock_get_provider = mocker.patch("wktplot.plots.osm.get_provider")

        plot = OpenStreetMapsPlot(title=PLOT_TITLE, save_dir=temp_dir, **STYLE_KWARGS)
        expected_kwargs = {
            **STYLE_KWARGS,
            **plot.default_figure_style_kwargs,
        }

        mock_get_provider.assert_called_once_with(Vendors.OSM)
        mock_bokeh.figure.assert_called_once_with(title=PLOT_TITLE, **expected_kwargs)
        plot.figure.add_tile.assert_called_once_with(mock_get_provider.return_value)
