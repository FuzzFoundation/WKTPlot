import logging
import sys
import typing as ty

from bokeh.plotting import figure, show, output_file, save
from pathlib import Path
from shapely import wkt
from shapely.geometry import BaseGeometry, GeometryCollection, LineString, LinearRing, MultiLineString, MultiPoint, MultiPolygon, Point, Polygon


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
        self.figure.toolbar.autohide = True

    def add_shape(self, shape: ty.Union[str, BaseGeometry]):
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
        elif isinstance(shape, GeometryCollection):
            for poly in shape:
                self.add_shape(poly)
        else:
            raise NotImplementedError(f"Given `shape` argument is of an unexpected type [{type(shape).__name__}]")

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
                x.append(point.x)
                y.append(point.y)
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
                _x, _y = map(list, line.xy)
                x.append(_x)
                y.append(_y)
            self.figure.multi_line(x, y, line_width=3)
        else:
            raise TypeError(f"Given `shape` argument is of an unexpected type [{type(shape).__name__}]")

    def _plot_polys(self, shape: ty.Union[Polygon, MultiPolygon]):
        """ TODO: docstring
        """
        if shape.is_empty:
            self.logger.info("Given shape is empty, returning.")
            return

        if not isinstance(shape, (Polygon, MultiPolygon)):
            raise TypeError(f"Given `shape` argument is of an unexpected type [{type(shape).__name__}]")

        x, y = self._get_poly_coordinates(shape)
        self.figure.multi_polygons([[x]], [[y]], line_width=3)
    
    def _get_poly_coordinates(self, shape: ty.Union[Polygon, MultiPolygon]):
        """ TODO: docstring
        """

        x, y = [], []
        if isinstance(shape, MultiPolygon):
            for poly in shape:
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
