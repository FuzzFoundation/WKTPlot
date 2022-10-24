from bokeh import plotting as plt
from pathlib import Path
from shapely.geometry.base import BaseGeometry
from typing import Any, Dict, Union
from wktplot.common.file_utils import get_random_string, sanitize_text
from wktplot.mappers.standard import StandardMapper
from wktplot.plots.base import BasePlot


class WKTPlot(BasePlot):
    """ Standard WKTPlot Bokeh wrapper class.
    """

    def __init__(
        self,
        title: str = get_random_string(),
        save_dir: Union[str, Path] = Path("."),
        **figure_style_kwargs: Dict[str, Any],
    ) -> None:
        """ Create figure with given arguments.

        Args:
            title (str): Title for graph and output filename, defaults to random string if unset.
            save_dir (str | obj: Path, default = "."): Optional path to save output file to.
            **figure_style_kwargs (dict[str, Any]): Dictionary of attributes to style the created figure.
                See this guide for available style attributes:
                https://docs.bokeh.org/en/2.4.3/docs/reference/plotting/figure.html

        Raises:
            ValueError: If value for `title` is not a string or None.
            OSError: If value for `save_dir` is not a directory.
        """

        if not isinstance(title, str):
            raise ValueError(f"Given argument `title` is not a string. [{title}]")

        if isinstance(save_dir, str):
            save_dir = Path(save_dir)

        if not (isinstance(save_dir, Path) and save_dir.is_dir()):
            raise OSError(f"Given argument `save_dir` is not a directory. [{save_dir}]")

        filename: Path = save_dir / f"{sanitize_text(title)}.html"
        plt.output_file(filename=filename, title=title, mode="inline")

        self.figure: plt.Figure = self._create_figure(title=title, **figure_style_kwargs)
        self.mapper = StandardMapper

    def add_shape(self, shape: Union[str, BaseGeometry], **style_kwargs: dict) -> None:
        self.mapper.add_shape(self.figure, shape, **style_kwargs)

    def save(self) -> None:
        plt.save(self.figure)

    def show(self) -> None:
        plt.show(self.figure)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @classmethod
    def _create_figure(cls, title: str, **style_kwargs: Dict[str, Any]) -> plt.Figure:

        default_kwargs: Dict[str, Any] = {
            "x_axis_label": "Longitude",
            "y_axis_label": "Latitude",
            **style_kwargs,
        }

        fig = plt.figure(title=title, **default_kwargs)
        fig.toolbar.autohide = True

        return fig
