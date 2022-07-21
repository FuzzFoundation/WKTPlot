from .base import BaseMap
from shapely.geometry import Point, LineString, LinearRing, Polygon
from typing import List, Tuple, Union


class StandardMap(BaseMap):

    @classmethod
    def get_point_coords(cls, shape: Point) -> Tuple[float, float]:

        return shape.x, shape.y
    
    @classmethod
    def get_line_string_coords(cls, shape: Union[LineString, LinearRing]) -> Tuple[List[float], List[float]]:

        x, y = map(list, shape.xy)
        return x, y
    
    @classmethod
    def get_polygon_coords(self, shape: Polygon) -> Tuple[List[List[float]], List[List[float]]]:

        ext_x, ext_y = map(list, shape.exterior.xy)

        # Shape coordinates start and end with the same value.
        # Chop off last coordinate for Bokeh.
        x: List[float] = [ext_x[:-1]]
        y: List[float] = [ext_y[:-1]]

        for intr_shape in shape.interiors:
            intr_x, intr_y = map(list, intr_shape.xy)

            x.append(intr_x[:-1])
            y.append(intr_y[:-1])
        
        return x, y