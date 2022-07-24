from abc import ABC, abstractclassmethod
from shapely.geometry import Point, LineString, LinearRing, Polygon
from typing import List, Tuple, Union


class BaseMapper(ABC):

    @abstractclassmethod
    def _get_point_coords(cls, shape: Point) -> Tuple[float, float]:
        """ Get x, y coordinate of the given `shape` geometry.

        Args:
            shape (obj: Point): Point shape.

        Returns:
            tuple[float, float]: Tuple with x, y coordinate values.
        """

    @abstractclassmethod
    def _get_line_string_coords(cls, shape: Union[LineString, LinearRing]) -> Tuple[List[int], List[int]]:
        """ Get x, y coordinates of the given `shape` geometry.

        Args:
            shape (obj: LineString | obj: LinearRing): LineString or LinearRing shape.

        Returns:
            tuple[list[float], list[float]]: Tuple with x, y coordinate value lists.
        """

    @abstractclassmethod
    def _get_polygon_coords(cls, shape: Polygon) -> Tuple[List[List[float]], List[List[float]]]:
        """ Get x, y coordinates of the given `shape` geometry.

        Args:
            shape (obj: Polygon): Polygon shape.

        Returns:
            tuple[list[list[float]], list[list[float]]]: Tuple with x, y coordinate values as 2D lists.
        """
