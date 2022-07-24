from bokeh import plotting as plt
from bokeh.tile_providers import Vendors, get_provider
from typing import Any, Dict
from wktplot.mappers.osm import OpenStreetMapper
from wktplot.plots.standard import WKTPlot


class OpenStreetMapsPlot(WKTPlot):
    """ OpenStreetMaps WKTPlot Bokeh wrapper class.
    """

    mapper = OpenStreetMapper
    default_figure_style_kwargs: Dict[str, str] = {
        "x_axis_type": "mercator",
        "y_axis_type": "mercator",
    }

    @classmethod
    def _create_figure(cls, title: str, **style_kwargs: Dict[str, Any]) -> plt.Figure:

        # Set axis type to load the map
        # - https://docs.bokeh.org/en/latest/docs/user_guide/geo.html#tile-provider-maps
        default_kwargs: Dict[str, Any] = {
            **style_kwargs,
            **cls.default_figure_style_kwargs,
        }

        tile_provider = get_provider(Vendors.OSM)
        fig = super()._create_figure(title=title, **default_kwargs)
        fig.add_tile(tile_provider)

        return fig
