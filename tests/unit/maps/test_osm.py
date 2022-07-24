from shapely import wkt
from wktplot.mappers.osm import OpenStreetMapper

import pytest


class TestGetPointCoords:

    def test_when_given_valid_point_returns_expected_coords(self):

        expected_coords = (1113194.90793, 3503549.84350)
        shape = wkt.loads("POINT (30 10)")
        assert OpenStreetMapper._get_point_coords(shape) == pytest.approx(expected_coords)


class TestGetLineStringCoords:

    def test_when_given_valid_line_returns_expected_coords(self):

        expected_coords = (
            [
                1113194.90793,
                3339584.72380,
                4452779.63173,
            ],
            [
                3503549.84350,
                1118889.97486,
                4865942.27950,
            ],
        )
        shape = wkt.loads("LINESTRING (30 10, 10 30, 40 40)")
        for actual, expected in zip(
            OpenStreetMapper._get_line_string_coords(shape),
            expected_coords
        ):
            assert actual == pytest.approx(expected)


class TestGetPolygonCoords:

    def test_when_given_valid_shape_returns_expected_coords(self):

        expected_coords = (
            [[
                1113194.90793,
                4452779.63173,
                4452779.63173,
                2226389.81587,
            ]],
            [[
                3503549.84350,
                4865942.27950,
                2273030.92699,
                1118889.97486,
            ]],
        )
        shape = wkt.loads("POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))")
        for actual, expected in zip(
            OpenStreetMapper._get_polygon_coords(shape),
            expected_coords
        ):
            assert actual[0] == pytest.approx(expected[0])
