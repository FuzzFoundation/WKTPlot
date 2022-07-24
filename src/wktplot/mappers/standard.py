from bokeh.plotting import Figure
from shapely import wkt
from shapely.geometry import Point, LineString, LinearRing, Polygon
from shapely.geometry.base import BaseGeometry, BaseMultipartGeometry
from typing import Any, Dict, List, Tuple, Union
from wktplot.common.types import SUPPORTED_GEOMS
from wktplot.mappers.base import BaseMapper


class StandardMapper(BaseMapper):

    @classmethod
    def _get_point_coords(cls, shape: Point) -> Tuple[float, float]:
        return shape.x, shape.y

    @classmethod
    def _get_line_string_coords(cls, shape: Union[LineString, LinearRing]) -> Tuple[List[float], List[float]]:
        x, y = map(list, shape.xy)
        return x, y

    @classmethod
    def _get_polygon_coords(self, shape: Polygon) -> Tuple[List[List[float]], List[List[float]]]:

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

    @classmethod
    def add_shape(cls, figure: Figure, shape: Union[str, BaseGeometry], **style_kwargs: Dict[str, Any]) -> None:

        if isinstance(shape, str):
            shape = wkt.loads(shape)

        if not isinstance(shape, SUPPORTED_GEOMS):
            raise TypeError(
                f"Given argument `shape` is of an unsupported type [{type(shape).__name__}]"
            )

        if shape.is_empty:
            return

        if isinstance(shape, BaseMultipartGeometry):
            for poly in shape.geoms:
                cls.add_shape(figure, poly, **style_kwargs)

        elif isinstance(shape, Point):
            x, y = cls._get_point_coords(shape)
            figure.circle(x, y, **style_kwargs)

        elif isinstance(shape, (LineString, LinearRing)):
            x, y = cls._get_line_string_coords(shape)
            figure.line(x, y, **style_kwargs)

        elif isinstance(shape, Polygon):
            x, y = cls._get_polygon_coords(shape)
            figure.multi_polygons([[x]], [[y]], **style_kwargs)
