from .common import PLOT_TITLE, STYLE_KWARGS
from bokeh.tile_providers import Vendors
from unittest.mock import MagicMock
from wktplot.plots.osm import OpenStreetMapsPlot


class TestConstructor:

    def test_when_given_valid_arguments_figure_class_var_set(
        self,
        mocker,
        mock_get_provider: MagicMock,
        mock_bokeh: MagicMock,
        mock_osm_plot: OpenStreetMapsPlot,
    ) -> None:

        expected_kwargs = {
            **STYLE_KWARGS,
            **mock_osm_plot.default_figure_style_kwargs,
        }
        mock_get_provider.assert_called_once_with(Vendors.OSM)
        mock_bokeh.figure.assert_called_once_with(
            title=PLOT_TITLE,
            **expected_kwargs,
        )
        mock_osm_plot.figure.add_tile.assert_called_once_with(mock_get_provider.return_value)
        

