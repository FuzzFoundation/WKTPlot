from abc import ABC, abstractclassmethod
from bokeh.plotting import Figure


class BaseFigure(ABC):
    
    @abstractclassmethod
    def create_figure(self) -> Figure:
        """ TODO: docstring
        """
    
