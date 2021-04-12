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

    def add_shape(self, shape, fill_color=None, stroke_color=None, name=None):
        """ TODO: docstring
        """
        pass
        # if isinstance(shape, str):
        #     shape = wkt.loads(shape)

        # fill_color = colors_dict.get(fill_color, "#00000000")
        # stroke_color = colors_dict.get(stroke_color, "#00000000")
        # if not fill_color and not stroke_color:
        #     print("No fill or stroke color.")
        #     return

        # if isinstance(shape, MultiLineString):
        #     for line_string in shape:
        #         self.plot_line(line_string, fill_color)
        # elif isinstance(shape, (LineString, Point)):
        #     self.plot_line(shape, fill_color)
        # elif isinstance(shape, MultiPolygon):
        #     for poly in shape:
        #         self.plot_poly(poly, fill_color, stroke_color)
        # elif isinstance(shape, Polygon):
        #     self.plot_poly(shape, fill_color, stroke_color)
        # elif isinstance(shape, GeometryCollection):
        #     for poly in shape:
        #         self.add_shape(poly, fill_color=fill_color, stroke_color=stroke_color)
        # else:
        #     print(type(shape))

        # self.save_wkt(shape.wkt, name)

    def add_shapes(self, shapes_list):
        """ TODO: docstring
        """
        pass
        # for item in shapes_list:
        #     self.add_shape(*item)
        # return self

    def plot_points(self, shape: ty.Union[Point, MultiPoint]):
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

    def plot_lines(self, shape: ty.Union[LineString, MultiLineString]):
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

    def plot_polys(self, shape: ty.Union[Polygon, MultiPolygon]):
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

    def clear(self):
        """ TODO: docstring
        """
        pass
        # self.fig.clf()
        # self.setup_axis()

    def save(self):
        """ TODO: docstring
        """
        save(self.figure)
        # self.ax.set_title(plot_name)
        # print(self.ax.get_xlim())
        # plot_name = plot_name.lower().replace(" ", "_")
        # fig_f = os.path.join(self.save_dir, f"{plot_name}.png")
        # if os.path.isfile(fig_f):
        #     os.remove(fig_f)
        # self.fig.tight_layout()
        # self.fig.savefig(fig_f)
        # return self

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
