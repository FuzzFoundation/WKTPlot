from abc import ABC, abstractmethod, abstractclassmethod
from bokeh.plotting import Figure
from shapely.geometry.base import BaseGeometry
from typing import Union


class BasePlot(ABC):

    @abstractclassmethod
    def _create_figure(cls) -> Figure:
        """ TODO: docstring
        """

    @abstractmethod
    def save(self) -> None:
        """ Wrapper method around `bokeh.plotting.save`.

        See source for more info:
        https://docs.bokeh.org/en/latest/docs/reference/io.html#bokeh.io.save
        """

    @abstractmethod
    def show(self) -> None:
        """ Wrapper method around `bokeh.plotting.show`.

        See source for more info:
        https://docs.bokeh.org/en/latest/docs/reference/io.html#bokeh.io.show
        """

    @abstractmethod
    def add_shape(self, shape: Union[str, BaseGeometry], **style_kwargs: dict) -> None:
        """ Plot a given well-known-text string or shapely object.

        Args:
            shape (str | obj: BaseGeometry): Shape to plot.
            **style_kwargs (dict): Dictionary of attributes to style the given shape.
                See this guide for available style attributes:
                https://docs.bokeh.org/en/latest/docs/user_guide/styling.html

        Raises:
            TypeError: When given `shape` type is not currently supported.
        """
