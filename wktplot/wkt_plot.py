import os
import string
import typing as ty

from time import time
from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource
from random import choice
from shapely import wkt
from shapely.geometry import GeometryCollection, LineString, MultiLineString, MultiPolygon, Point, Polygon


class WKTPlot:
    def __init__(self, title: ty.Optional[str]):
        """ TODO: docstring
        """
        if title is None:
            title = f"{int(time())}"
        self.figure = figure(title=title, x_axis_label="Longitude", y_axis_label="Latitude")

    def plot_line(self, obj, fill_color):
        """
        Plot given LineString `obj`, filled with given `color`.

        Args:
            obj (shapely.LineString): LineString to plot.
            color (str): Color hex-string from `matplotlib.colors.CSS4_COLORS` dictionary.
        """
        if not obj.is_empty:
            x, y = obj.xy
            self.ax.plot(
                x, y, color=fill_color, linewidth=10, solid_capstyle='round', zorder=self.__zorder)
            self.__zorder += 1

    def plot_poly(self, obj, fill_color, stroke_color):
        """ TODO: docstring
        """
        pass
        # patch = PolygonPatch(obj, fc=fill_color, ec=stroke_color, zorder=self.__zorder)
        # self.ax.add_patch(patch)
        # self.ax.plot()
        # self.__zorder += 1

    def add_geodataframe(self, gdf, fill_color=None, stroke_color=None, name=None):
        """ TODO: docstring
        """
        pass
        # fill_color = colors_dict.get(fill_color, "#FFFFFFFF")
        # stroke_color = colors_dict.get(stroke_color, "#FFFFFFFF")
        # gdf.plot(ax=self.ax, fc=fill_color, ec=stroke_color, zorder=self.__zorder)
        # self.__zorder += 1

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

    def clear(self):
        """ TODO: docstring
        """
        pass
        # self.fig.clf()
        # self.setup_axis()

        """

    def save(self, plot_name):
        """
        Save figure to .png image.
        """
        self.ax.set_title(plot_name)
        print(self.ax.get_xlim())
        plot_name = plot_name.lower().replace(" ", "_")
        fig_f = os.path.join(self.save_dir, f"{plot_name}.png")
        if os.path.isfile(fig_f):
            os.remove(fig_f)
        self.fig.tight_layout()
        self.fig.savefig(fig_f)
        return self

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
