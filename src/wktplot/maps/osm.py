from bokeh.plotting import Figure
from bokeh.tile_providers import get_provider, Vendors
from typing import Any, Dict
from wktplot import WKTPlot

SCALE: int = 10 ** 5


class OpenStreetMapPlot(WKTPlot):

    def create_figure(self, title: str, **figure_style_kwargs: Dict[str, Any]) -> Figure:
        """ TODO: docstring
        """

        # Set axis type to load the map
        # - https://docs.bokeh.org/en/latest/docs/user_guide/geo.html#tile-provider-maps
        default_kwargs: Dict[str, Any] = {
            "x_axis_type": "mercator",
            "y_axis_type": "mercator",
        }

        default_kwargs.update(figure_style_kwargs)

        tile_provider = get_provider(Vendors.OSM)
        fig: Figure = super().create_figure(title, **default_kwargs)
        fig.add_tile(tile_provider)

        return fig
    

