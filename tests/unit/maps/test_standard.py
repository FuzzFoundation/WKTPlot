from .common import STYLE_KWARGS
from shapely import wkt
from shapely.geometry.base import BaseGeometry
from unittest.mock import call, MagicMock
from wktplot.maps.standard import StandardMap

import pytest


class FakeShape(BaseGeometry):
    """ Fake shapely shape to test NotImplementedError unittests.
    """

    @property
    def is_empty(self):
        return False


class TestGetPointCoords:

    def test_when_given_valid_point_returns_expected_coords(self):

        expected_coords = (30.0, 10.0)
        shape = wkt.loads("POINT (30 10)")
        assert StandardMap._get_point_coords(shape) == expected_coords


class TestGetLineStringCoords:

    def test_when_given_valid_line_returns_expected_coords(self):

        expected_coords = ([30, 10, 40], [10, 30, 40])
        shape = wkt.loads("LINESTRING (30 10, 10 30, 40 40)")
        assert StandardMap._get_line_string_coords(shape) == expected_coords


class TestGetPolygonCoords:

    def test_when_given_valid_shape_returns_expected_coords(self):

        expected_coords = (
            [[30.0, 40.0, 20.0, 10.0]],
            [[10.0, 40.0, 40.0, 20.0]],
        )
        shape = wkt.loads("POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))")
        assert StandardMap._get_polygon_coords(shape) == expected_coords


class TestAddShape:

    def test_when_given_unsupported_shape_raises_TypeError(
        self,
        mock_figure: MagicMock,
    ) -> None:

        shape = FakeShape()
        with pytest.raises(TypeError):
            StandardMap.add_shape(mock_figure, shape)

    def test_when_given_empty_shape_returns_early(
        self,
        mock_figure: MagicMock,
    ) -> None:

        empty_shape = wkt.loads("POINT EMPTY")
        StandardMap.add_shape(mock_figure, empty_shape)
        mock_figure.circle.assert_not_called()

    def test_when_given_valid_point_calls_expected_methods(
        self,
        mock_figure: MagicMock,
    ) -> None:

        shape = wkt.loads("POINT (30 10)")
        StandardMap.add_shape(mock_figure, shape, **STYLE_KWARGS)
        mock_figure.circle.assert_called_once_with(30, 10, **STYLE_KWARGS)

    def test_when_given_valid_linestring_calls_expected_methods(
        self,
        mock_figure: MagicMock,
    ) -> None:

        shape = wkt.loads("LINESTRING (30 10, 10 30, 40 40)")
        StandardMap.add_shape(mock_figure, shape, **STYLE_KWARGS)
        mock_figure.line.assert_called_once_with(
            [30, 10, 40],
            [10, 30, 40],
            **STYLE_KWARGS,
        )

    def test_when_given_valid_linearring_calls_expected_methods(
        self,
        mock_figure: MagicMock,
    ) -> None:

        shape = wkt.loads("LINEARRING (10 20, 20 25, 35 50, 10 20)")
        StandardMap.add_shape(mock_figure, shape, **STYLE_KWARGS)
        mock_figure.line.assert_called_once_with(
            [10, 20, 35, 10],
            [20, 25, 50, 20],
            **STYLE_KWARGS,
        )

    def test_when_given_valid_polygon_calls_expected_methods(
        self,
        mock_figure: MagicMock,
    ) -> None:

        shape = wkt.loads("POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))")
        StandardMap.add_shape(mock_figure, shape, **STYLE_KWARGS)
        mock_figure.multi_polygons.assert_called_once_with(
            [[[[30.0, 40.0, 20.0, 10.0]]]],
            [[[[10.0, 40.0, 40.0, 20.0]]]],
            **STYLE_KWARGS,
        )

    def test_when_given_valid_multipoint_calls_expected_methods(
        self,
        mock_figure: MagicMock,
    ) -> None:

        shape = wkt.loads("MULTIPOINT ((10 40), (40 30), (20 20), (30 10))")
        StandardMap.add_shape(mock_figure, shape, **STYLE_KWARGS)
        mock_figure.circle.assert_has_calls([
            call(10, 40, **STYLE_KWARGS),
            call(40, 30, **STYLE_KWARGS),
            call(20, 20, **STYLE_KWARGS),
            call(30, 10, **STYLE_KWARGS),
        ])

    def test_when_given_valid_multilinestring_calls_expected_methods(
        self,
        mock_figure: MagicMock,
    ) -> None:

        shape = wkt.loads("MULTILINESTRING ((10 10, 20 20, 10 40), (40 40, 30 30, 40 20, 30 10))")
        StandardMap.add_shape(mock_figure, shape, **STYLE_KWARGS)
        mock_figure.line.assert_has_calls([
            call([10, 20, 10], [10, 20, 40], **STYLE_KWARGS),
            call([40, 30, 40, 30], [40, 30, 20, 10], **STYLE_KWARGS),
        ])

    def test_when_given_valid_multipolygon_calls_expected_methods(
        self,
        mock_figure: MagicMock,
    ) -> None:

        shape = wkt.loads("MULTIPOLYGON (((30 20, 45 40, 10 40, 30 20)), ((15 5, 40 10, 10 20, 5 10, 15 5)))")
        StandardMap.add_shape(mock_figure, shape, **STYLE_KWARGS)
        mock_figure.multi_polygons.assert_has_calls([
            call([[[[30.0, 45.0, 10.0]]]], [[[[20.0, 40.0, 40.0]]]], **STYLE_KWARGS),
            call([[[[15.0, 40.0, 10.0, 5.0]]]], [[[[5.0, 10.0, 20.0, 10.0]]]], **STYLE_KWARGS),
        ])
