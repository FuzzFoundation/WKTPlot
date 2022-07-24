import numpy as np

from shapely.geometry import Point, LineString, LinearRing, Polygon
from typing import List, Tuple, Union
from wktplot.mappers.standard import StandardMapper


EARTH_RADIUS: float = 6378137.0
COORDINATES = Union[float, np.float64, np.ndarray]


def geographic_to_mercator(lat_deg: COORDINATES, lng_deg: COORDINATES) -> Tuple[COORDINATES, COORDINATES]:
    """ Convert given lat / long coordinates to mercator coordinates.
        - https://en.wikipedia.org/wiki/Mercator_projection#Derivation
        - https://en.wikipedia.org/wiki/Transverse_Mercator_projection#Formulae_for_the_spherical_transverse_Mercator

    Args:
        lat_deg (float | obj: np.ndarray): Latitude coordinates in degrees.
        lng_deg (float | obj: np.ndarray): Longitude coordinates in degrees.

    Return:
        tuple[float | obj: np.ndarray, float | obj: np.ndarray]: Tuple containing longitude and latitude mercator
            coordinates.
    """

    φ = np.radians(lat_deg)
    λ = np.radians(lng_deg)

    merc_lat = EARTH_RADIUS * np.log(np.tan((np.pi / 4.0) + (φ / 2.0)))
    merc_lng = EARTH_RADIUS * λ

    return merc_lng, merc_lat


class OpenStreetMapper(StandardMapper):

    @classmethod
    def _get_point_coords(cls, shape: Point) -> Tuple[float, float]:

        geo_x, geo_y = super()._get_point_coords(shape)
        merc_x, merc_y = map(
            float,
            geographic_to_mercator(
                lat_deg=geo_x,
                lng_deg=geo_y,
            )
        )

        return merc_x, merc_y

    @classmethod
    def _get_line_string_coords(cls, shape: Union[LineString, LinearRing]) -> Tuple[List[float], List[float]]:

        geo_x_list, geo_y_list = super()._get_line_string_coords(shape)

        merc_x, merc_y = map(
            list,
            geographic_to_mercator(
                lat_deg=np.array(geo_x_list, dtype=float),
                lng_deg=np.array(geo_y_list, dtype=float),
            )
        )
        return merc_x, merc_y

    @classmethod
    def _get_polygon_coords(cls, shape: Polygon) -> Tuple[List[List[float]], List[List[float]]]:

        merc_x_nested_list: List[List[float]] = []
        merc_y_nested_list: List[List[float]] = []

        geo_x_nested_list, geo_y_nested_list = super()._get_polygon_coords(shape)

        for geo_x_list, geo_y_list in zip(geo_x_nested_list, geo_y_nested_list):
            merc_x_arr, merc_y_arr = map(
                list,
                geographic_to_mercator(
                    lat_deg=np.array(geo_x_list, dtype=float),
                    lng_deg=np.array(geo_y_list, dtype=float),
                )
            )
            merc_x_nested_list.append(merc_x_arr)
            merc_y_nested_list.append(merc_y_arr)

        return merc_x_nested_list, merc_y_nested_list
