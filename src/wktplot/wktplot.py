import logging
import sys

from bokeh.plotting import Figure, output_file, save, show
from pathlib import Path
from shapely import wkt
from shapely.geometry import (
    GeometryCollection,
    LineString,
    LinearRing,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)
from shapely.geometry.base import BaseGeometry, BaseMultipartGeometry
from typing import Any, Dict, List, Optional, Tuple, Type, Union
from wktplot.file_utils import get_random_string, sanitize_text
from wktplot.figures import StandardFigure
from wktplot.maps import StandardMap


SUPORTED_GEOMS: Tuple[Type[BaseGeometry]] = (
    GeometryCollection,
    LineString,
    LinearRing,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s : %(lineno)d - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)


class WKTPlot(StandardFigure, StandardMap):
    logger = logging.getLogger(__name__)

    def __init__(
        self,
        title: Optional[str] = None,
        save_dir: Union[str, Path] = None,
        **figure_style_kwargs: Dict[str, Any],
    ) -> None:
        """ Constructor for WKTPlot class.

        Args:
            title (str | None): Title for graph and output filename, defaults to random string if None.
            save_dir (str | obj: Path): Path to save output file to.
            **figure_style_kwargs (dict[str, Any]): Dictionary of attributes to style the created figure.
                See this guide for available style attributes:
                https://docs.bokeh.org/en/2.4.3/docs/reference/plotting/figure.html

        Raises:
            OSError: If value for `save_dir` is not a directory.
            ValueError: If value for `title` is not a string or None.
        """

        if isinstance(save_dir, str):
            save_dir = Path(save_dir)

        if not (isinstance(save_dir, Path) and save_dir.is_dir()):
            raise OSError(f"Given argument `save_dir` is not a directory. [{save_dir=}]")
        
        if title is not None and not isinstance(title, str):
            raise ValueError(f"Given argument `title` is not a string. [{title=}]")

        elif title is None:
            title = get_random_string()
        
        title: str = sanitize_text(title)
        filename: Path = save_dir / f"{title}.html"

        output_file(filename=filename, title=title, mode="inline")
        self.figure: Figure = self.create_figure(title=title, **figure_style_kwargs)
    
    def add_shape(self, shape: Union[str, BaseGeometry], **style_kwargs: dict):
        """ Plot a given well-known-text string or shapely object. Shapely geometries currently supported are:
            - `GeometryCollection`
            - `LineString`
            - `LinearRing`
            - `MultiLineString`
            - `MultiPoint`
            - `MultiPolygon`
            - `Point`
            - `Polygon`

        Args:
            shape (str | obj: BaseGeometry): Shape to plot.
            **style_kwargs (dict): Dictionary of attributes to style the given shape.
                See this guide for available style attributes:
                https://docs.bokeh.org/en/latest/docs/user_guide/styling.html

        Raises:
            TypeError: When given `shape` type is not currently supported.
        """

        if isinstance(shape, str):
            shape = wkt.loads(shape)

        if not isinstance(shape, SUPORTED_GEOMS):
            raise TypeError(f"Given argument `shape` is of an unsupported type [{type(shape).__name__}]")

        if shape.is_empty:
            self.logger.info("Given shape is empty, returning.")
            return

        if isinstance(shape, BaseMultipartGeometry):
            for poly in shape.geoms:
                self.add_shape(poly, **style_kwargs)
        
        elif isinstance(shape, Point):
            x, y = self.get_point_coords(shape)
            self.figure.circle(x, y, **style_kwargs)
        
        elif isinstance(shape, (LineString, LinearRing)):
            x, y = self.get_line_string_coords(shape)
            self.figure.line(x, y, **style_kwargs)
        
        elif isinstance(shape, Polygon):
            x, y = self.get_polygon_coords(shape)
            self.figure.multi_polygons([[x]], [[y]], **style_kwargs)

    def save(self):
        """ Wrapper method around `bokeh.plotting.save`.

        See source for more info: https://docs.bokeh.org/en/latest/docs/reference/io.html#bokeh.io.save
        """

        save(self.figure)

    def show(self):
        """ Wrapper method around `bokeh.plotting.show`.

        See source for more info: https://docs.bokeh.org/en/latest/docs/reference/io.html#bokeh.io.show
        """

        show(self.figure)
