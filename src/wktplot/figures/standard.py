from .base import BaseFigure
from bokeh.plotting import Figure, figure
from typing import Any, Dict 


class StandardFigure(BaseFigure):

    @classmethod
    def create_figure(cls, title: str, **style_kwargs: Dict[str, Any]) -> Figure:

        default_kwargs: Dict[str, Any] = {
            "x_axis_label": "Longitude",
            "y_axis_label": "Latitude",
            **style_kwargs,
        }

        fig = figure(title=title, **default_kwargs)
        fig.toolbar.autohide = True

        return fig