from .common import PLOT_TITLE, STYLE_KWARGS
from bokeh.tile_providers import Vendors
from pytest_mock import MockFixture
from unittest.mock import MagicMock
from wktplot.mappers.standard import StandardMapper
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

        mock_get_provider.assert_called_once_with(Vendors.OSM)
        mock_bokeh.figure.assert_called_once_with(
            title=PLOT_TITLE,
            **STYLE_KWARGS,
            x_axis_type="mercator",
            y_axis_type="mercator",
            x_axis_label="Longitude",
            y_axis_label="Latitude",
        )
        plot.figure.add_tile.assert_called_once_with(mock_get_provider.return_value)

    def test_when_disable_mercator_set_mapped_set_to_Standard(self):
        
        plot = OpenStreetMapsPlot(disable_mercator=True)
        assert plot.mapper == StandardMapper
