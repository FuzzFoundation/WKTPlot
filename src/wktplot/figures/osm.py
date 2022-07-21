from .base import BaseFigure
from bokeh.plotting import Figure, figure
from bokeh.tile_providers import Vendors, get_provider
from typing import Any, Dict


class OpenStreetMapsFigure(BaseFigure):

    @classmethod    
    def create_figure(cls, title: str, **style_kwargs: Dict[str, Any]) -> Figure:

        # Set axis type to load the map
        # - https://docs.bokeh.org/en/latest/docs/user_guide/geo.html#tile-provider-maps
        default_kwargs: Dict[str, Any] = {
            **style_kwargs,
            "x_axis_type": "mercator",
            "y_axis_type": "mercator",
        }

        fig = figure(title=title, **default_kwargs)
        fig.toolbar.autohide = True

        tile_provider = get_provider(Vendors.OSM)
        fig.add_tile(tile_provider)

        return fig