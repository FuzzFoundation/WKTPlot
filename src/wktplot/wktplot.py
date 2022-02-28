import logging
import sys

from abc import ABC, abstractmethod
from bokeh.plotting import Figure, figure, output_file, save, show
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
from shapely.geometry.base import BaseGeometry
from typing import Any, Dict, Union
from wktplot.file_utils import get_random_string, sanitize_text


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s : %(lineno)d - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)


class WKTPlot(ABC):
    logger = logging.getLogger(__name__)

    def __init__(
        self,
        title: str = None,
        save_dir: Union[str, Path] = None,
        **figure_style_kwargs: Dict[str, Any],
    ) -> None:
        """ Constructor for WKTPlot class.

        Args:
            title (str): Title for graph and output filename.
                e.g. title = "Test 123 ABC" -> filename = "test_123_abc.html"
            save_dir (str | obj: Path): Path to save output file to.

        Raises:
            OSError: If value for `save_dir` is not a directory.
        """

        if isinstance(save_dir, str):
            save_dir = Path(save_dir)

        if not (isinstance(save_dir, Path) and save_dir.is_dir()):
            raise OSError(f"Given argument `save_dir` is not a directory. [{save_dir}]")

        if not title:
            title: str = get_random_string()
            self.logger.info(f"Given title is empty, setting title to [{title}]")
        
        title: str = sanitize_text(title)
        filename: Path = save_dir / f"{title}.html"

        output_file(filename=filename, title=title, mode="inline")
        self.figure: Figure = self.create_figure(title=title, **figure_style_kwargs)
    
    @abstractmethod
    def create_figure(self, title: str, **figure_style_kwargs: Dict[str, Any]) -> Figure:
        """ TODO: docstring
        """

        default_kargs: Dict[str, Any] = {
            "x_axis_label": "Longitude",
            "y_axis_label": "Latitude",
        }

        default_kargs.update(figure_style_kwargs)

        fig = figure(title=title, **default_kargs)
        fig.toolbar.autohide = True

        return fig

    def add_shape(self, shape: Union[str, BaseGeometry], **style_kwargs: dict):
        """ Plot a given well-known-text string or shapely object. Shapely geometries currently supported are:
            `GeometryCollection`, `LineString`, `LinearRing`, `MultiLineString`, `MultiPoint`, `MultiPolygon`,
            `Point`, and `Polygon`.

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

        if shape.is_empty:
            self.logger.info("Given shape is empty, returning.")
            return

        if isinstance(shape, (Point, MultiPoint)):
            self._plot_points(shape, **style_kwargs)
        elif isinstance(shape, (LineString, MultiLineString, LinearRing)):
            self._plot_lines(shape, **style_kwargs)
        elif isinstance(shape, (Polygon, MultiPolygon)):
            self._plot_polys(shape, **style_kwargs)
        elif isinstance(shape, GeometryCollection):
            for poly in shape.geoms:
                self.add_shape(poly, **style_kwargs)
        else:
            raise NotImplementedError(f"Given `shape` argument is of an unexpected type [{type(shape).__name__}]")

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

    def _plot_points(self, shape: Union[str, Point, MultiPoint], **style_kwargs: dict):
        """ Internal method for plotting given non-empty, Point or MultiPoint `shape` object.

        Args:
            shape (str | obj: Point | obj: MultiPoint): Shape to plot.
            **style_kwargs (dict): Dictionary of attributes to style the given shape.
                See this guide for available style attributes:
                https://docs.bokeh.org/en/latest/docs/user_guide/styling.html

        Raises:
            TypeError: When given `shape` is not a `Point` or `MultiPoint` shapely geometry.
        """

        if shape.is_empty:
            self.logger.info("Given shape is empty, returning.")
            return

        x, y = [], []
        if isinstance(shape, MultiPoint):
            for point in shape.geoms:
                x.append(point.x)
                y.append(point.y)
        elif isinstance(shape, Point):
            x, y = map(list, shape.xy)
        else:
            raise TypeError(f"Given `shape` argument is of an unexpected type [{type(shape).__name__}]")

        self.figure.circle(x, y, **style_kwargs)

    def _plot_lines(self, shape: Union[LineString, MultiLineString, LinearRing], **style_kwargs: dict):
        """ Internal method for plotting given non-empty, LineString, MultiLineString, or LinearRing `shape` object.

        Args:
            shape (str | obj: LineString | obj: MultiLineString, | obj: LinearRing): Shape to plot.
            **style_kwargs (dict): Dictionary of attributes to style the given shape.
                See this guide for available style attributes:
                https://docs.bokeh.org/en/latest/docs/user_guide/styling.html

        Raises:
            TypeError: When given `shape` is not a `LineString`, `MultiLineString`, or `LinearRing` shapely geometry.
        """

        if shape.is_empty:
            self.logger.info("Given shape is empty, returning.")
            return

        if isinstance(shape, (LineString, LinearRing)):
            x, y = map(list, shape.xy)
            self.figure.line(x, y, **style_kwargs)
        elif isinstance(shape, MultiLineString):
            x, y = [], []
            for line in shape.geoms:
                _x, _y = map(list, line.xy)
                x.append(_x)
                y.append(_y)
            self.figure.multi_line(x, y, **style_kwargs)
        else:
            raise TypeError(f"Given `shape` argument is of an unexpected type [{type(shape).__name__}]")

    def _plot_polys(self, shape: Union[Polygon, MultiPolygon], **style_kwargs: dict):
        """ Internal method for plotting given non-empty, Polygon or MultiPolygon `shape` object.

        Args:
            shape (str | obj: Polygon | obj: MultiPolygon): Shape to plot.
            **style_kwargs (dict): Dictionary of attributes to style the given shape.
                See this guide for available style attributes:
                https://docs.bokeh.org/en/latest/docs/user_guide/styling.html

        Raises:
            TypeError: When given `shape` is not a `Polygon` or `MultiPolygon` shapely geometry.
        """

        if shape.is_empty:
            self.logger.info("Given shape is empty, returning.")
            return

        if not isinstance(shape, (Polygon, MultiPolygon)):
            raise TypeError(f"Given `shape` argument is of an unexpected type [{type(shape).__name__}]")

        x, y = self._get_poly_coordinates(shape)
        self.figure.multi_polygons([[x]], [[y]], **style_kwargs)

    def _get_poly_coordinates(self, shape: Union[Polygon, MultiPolygon]):
        """ Internal method for translating shapely polygon coordinates to bokeh polygon plotting coordinates.

        See this guide for more info:
        https://docs.bokeh.org/en/latest/docs/user_guide/plotting.html#multiple-multi-polygons

        Args:
            shape (str | obj: Polygon | obj: MultiPolygon): Shape to plot.

        Raises:
            TypeError: When given `shape` is not a `Polygon` or `MultiPolygon` shapely geometry.
        """

        x, y = [], []
        if isinstance(shape, MultiPolygon):
            for poly in shape.geoms:
                poly_x, poly_y = self._get_poly_coordinates(poly)
                x += poly_x
                y += poly_y
            return x, y

        elif isinstance(shape, Polygon):
            extr_x, extr_y = map(list, shape.exterior.xy)
            intr_x, intr_y = [], []
            for i in shape.interiors:
                _x, _y = map(list, i.xy)
                intr_x.append(_x[:-1])
                intr_y.append(_y[:-1])
            combined_x, combined_y = [extr_x[:-1]], [extr_y[:-1]]
            combined_x += intr_x
            combined_y += intr_y
            return combined_x, combined_y

        else:
            raise TypeError(f"Given `shape` argument is of an unexpected type [{type(shape).__name__}]")

