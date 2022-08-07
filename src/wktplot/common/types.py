from shapely.geometry import (
    GeometryCollection,
    LineString,
    LinearRing,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)
from shapely.geometry.base import BaseGeometry
from typing import Tuple, Type


SUPPORTED_GEOMS: Tuple[Type[BaseGeometry]] = (
    GeometryCollection,
    LineString,
    LinearRing,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)
