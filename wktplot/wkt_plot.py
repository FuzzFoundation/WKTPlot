import logging
import sys
import typing as ty

from bokeh.plotting import figure, show, output_file, save
from pathlib import Path
from shapely import wkt
from shapely.geometry import GeometryCollection, LineString, LinearRing, MultiLineString, MultiPoint, MultiPolygon, Point, Polygon


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s : %(lineno)d - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)


class WKTPlot:
    logger = logging.getLogger(__name__)

    def __init__(self, title: str, save_dir: ty.Union[str, Path]):
        """ TODO: docstring
        """
        if isinstance(save_dir, str):
            save_dir = Path(save_dir)
        if not save_dir.is_dir():
            raise OSError("Given argument `save_dir` is not a directory.")

        output_file(save_dir / f"{title.lower().replace(' ', '_')}.html", title=title, mode="inline")
        self.figure = figure(title=title, x_axis_label="Longitude", y_axis_label="Latitude")

    def add_shape(self, shape: ty.Union[str, GeometryCollection, LineString, LinearRing, MultiLineString, MultiPoint, MultiPolygon, Point, Polygon]):
        """ TODO: docstring
        """
        if isinstance(shape, str):
            shape = wkt.loads(shape)
        
        if shape.is_empty:
            self.logger.info("Given shape is empty, returning.")
            return
        
        if isinstance(shape, (Point, MultiPoint)):
            self._plot_points(shape)
        elif isinstance(shape, (LineString, MultiLineString, LinearRing)):
            self._plot_lines(shape)
        elif isinstance(shape, (Polygon, MultiPolygon)):
            self._plot_polys(shape)
        else:
            raise TypeError(f"Given `shape` argument is of an unexpected type [{type(shape).__name__}]")

    def add_shapes(self, shapes):
        """ TODO: docstring
        """
        for shape in shapes:
            self.add_shape(shape)
    
    def save(self):
        """ TODO: docstring
        """
        save(self.figure)
    
    def show(self):
        """ TODO: docstring
        """
        show(self.figure)

    def _plot_points(self, shape: ty.Union[str, Point, MultiPoint]):
        """ TODO: docstring
        """
        if shape.is_empty:
            self.logger.info("Given shape is empty, returning.")
            return

        x, y = [], []
        if isinstance(shape, MultiPoint):
            for point in shape:
                x += list(point.x)
                y += list(point.y)
        elif isinstance(shape, Point):
            x, y = map(list, shape.xy)
        else:
            raise TypeError(f"Given `shape` argument is of an unexpected type [{type(shape).__name__}]")
    
        self.figure.circle(x, y, line_width=3)

    def _plot_lines(self, shape: ty.Union[LineString, MultiLineString, LinearRing]):
        """ TODO: docstring
        """
        if shape.is_empty:
            self.logger.info("Given shape is empty, returning.")
            return

        if isinstance(shape, (LineString, LinearRing)):
            x, y = map(list, shape.xy)
            self.figure.line(x, y, line_width=3)
        elif isinstance(shape, MultiLineString):
            x, y = [], []
            for line in shape:
                x += list(line.x)
                y += list(line.y)
            self.figure.multi_line(x, y, line_width=3)
        else:
            raise TypeError(f"Given `shape` argument is of an unexpected type [{type(shape).__name__}]")

    def _plot_polys(self, shape: ty.Union[Polygon, MultiPolygon]):
        """ TODO: docstring
        """
        if shape.is_empty:
            self.logger.info("Given shape is empty, returning.")
            return

        if isinstance(shape, Polygon):
            x, y = map(list, shape.xy)
            self.figure.patch(x, y, line_width=3)
        elif isinstance(shape, MultiPolygon):
            x, y = [], []
            for poly in shape:
                x += list(poly.x)
                y += list(poly.y)
            self.figure.multi_polygons(x, y, line_width=3)
        else:
            raise TypeError(f"Given `shape` argument is of an unexpected type [{type(shape).__name__}]")

    def add_geodataframe(self, gdf, fill_color=None, stroke_color=None, name=None):
        """ TODO: docstring
        """
        pass
        # fill_color = colors_dict.get(fill_color, "#FFFFFFFF")
        # stroke_color = colors_dict.get(stroke_color, "#FFFFFFFF")
        # gdf.plot(ax=self.ax, fc=fill_color, ec=stroke_color, zorder=self.__zorder)
        # self.__zorder += 1

    def save_wkt(self, wkt, name):
        """ TODO: docstring
        """
        pass
        # if name is not None:
        #     if not os.path.isdir(self.wkt_dir):
        #         os.mkdir(self.wkt_dir)
        #     name = name.lower().replace(" ", "_")
        #     wkt_f = os.path.join(self.wkt_dir, f"{name}.txt")
        #     if os.path.isfile(wkt_f):
        #         os.remove(wkt_f)
        #     with open(wkt_f, "w+") as wf:
        #         wf.write(wkt)
