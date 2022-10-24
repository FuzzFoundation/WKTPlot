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

    def __init__(self, *args, disable_mercator: bool = False, **kwargs) -> None:
        """ Create figure with given arguments.

        Args:
            title (str): Title for graph and output filename, defaults to random string if unset.
            save_dir (str | obj: Path | None, default = None): Optional path to save output file to.
            disable_mercator (bool, default=False): Disable mercator proction calculation for shape data.
            **figure_style_kwargs (dict[str, Any]): Dictionary of attributes to style the created figure.
                See this guide for available style attributes:
                https://docs.bokeh.org/en/2.4.3/docs/reference/plotting/figure.html

        Raises:
            ValueError: If value for `title` is not a string or None.
            OSError: If value for `save_dir` is not a directory.
        """

        self.mapper.disable_mercator = disable_mercator
        super().__init__(*args, **kwargs)

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
