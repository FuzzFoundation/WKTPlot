from shapely import wkt
from unittest.mock import Mock, patch
from wktplot.wkt_plot import WKTPlot

import logging
import unittest

PLOT_TITLE = "test_1234"
PLOT_SAVE_DIR = "/tmp/mock_me_up_scotty"
STYLE_KWARGS = {"color": "MidnightBlue", "line_width": 3.0}

class InternalFunctionTests(unittest.TestCase):

    @patch("wktplot.wkt_plot.Path")
    @patch("wktplot.wkt_plot.output_file", Mock())
    @patch("wktplot.wkt_plot.figure", Mock())
    def setup_plot(self, mock_path):
        mock_path.return_value.is_dir.return_value = True
        plot = WKTPlot(title=PLOT_TITLE, save_dir=PLOT_SAVE_DIR)
        plot.figure.circle.reset_mock()
        plot.figure.line.reset_mock()
        plot.figure.multi_line.reset_mock()
        plot.figure.multi_polygons.reset_mock()
        return plot


    # --- _plot_points tests ---
    def test__plot_points__verify_point(self):
        """ Verify `_plot_points` calls methods with expected arguments when given `Point` shape.
        """
        test_plot = self.setup_plot()

        test_plot._plot_points(wkt.loads("POINT (30 10)"), **STYLE_KWARGS)
        expected_x = [30]
        expected_y = [10]
        test_plot.figure.circle.assert_called_once_with(expected_x, expected_y, **STYLE_KWARGS)

    def test__plot_points__verify_multipoint(self):
        """ Verify `_plot_points` calls methods with expected arguments when given `MultiPoint` shape.
        """
        test_plot = self.setup_plot()
        test_plot._plot_points(wkt.loads("MULTIPOINT ((10 40), (40 30), (20 20), (30 10))"), **STYLE_KWARGS)
        expected_x = [10, 40, 20, 30]
        expected_y = [40, 30, 20, 10]
        test_plot.figure.circle.assert_called_once_with(expected_x, expected_y, **STYLE_KWARGS)
    
    def test__plot_points__verify_empty(self):
        """ Verify `_plot_points` calls methods with expected arguments when given empty shape.
        """
        test_plot = self.setup_plot()
        with patch.object(test_plot, "logger", Mock(spec=logging)) as mock_logger:
            test_plot._plot_points(wkt.loads("POINT EMPTY"), **STYLE_KWARGS)
            mock_logger.info.assert_called_once_with("Given shape is empty, returning.")
            test_plot.figure.circle.assert_not_called()
    
    def test__plot_points__verify_unexpected_shape_raises_TypeError(self):
        """ Verify `_plot_points` raises TypeError when given unexpected shape.
        """
        test_plot = self.setup_plot()
        with self.assertRaises(TypeError) as e:
            test_plot._plot_points(wkt.loads("POLYGON ((1 0, 1 1, 0 1, 0 0, 1 0))"), **STYLE_KWARGS)
        self.assertIn("Given `shape` argument is of an unexpected type [Polygon]", e.exception.args)
    
    # --- _plot_lines tests ---
    def test__plot_lines__verify_linestring(self):
        """ Verify `_plot_lines` calls methods with expected arguments when given `LineString` shape.
        """
        test_plot = self.setup_plot()
        test_plot._plot_lines(wkt.loads("LINESTRING (30 10, 10 30, 40 40)"), **STYLE_KWARGS)
        expected_x = [30, 10, 40]
        expected_y = [10, 30, 40]
        test_plot.figure.line.assert_called_once_with(expected_x, expected_y, **STYLE_KWARGS)
    
    def test__plot_lines__verify_linear_ring(self):
        """ Verify `_plot_lines` calls methods with expected arguments when given `LinearRing` shape.
        """
        test_plot = self.setup_plot()
        test_plot._plot_lines(wkt.loads("LINEARRING (10 20, 20 25, 35 50, 10 20)"), **STYLE_KWARGS)
        expected_x = [10, 20, 35, 10]
        expected_y = [20, 25, 50, 20]
        test_plot.figure.line.assert_called_once_with(expected_x, expected_y, **STYLE_KWARGS)

    def test__plot_lines__verify_multilinestring(self):
        """ Verify `_plot_lines` calls methods with expected arguments when given `MultiLineString` shape.
        """
        test_plot = self.setup_plot()
        test_plot._plot_lines(wkt.loads("MULTILINESTRING ((10 10, 20 20, 10 40), (40 40, 30 30, 40 20, 30 10))"), **STYLE_KWARGS)
        expected_x = [[10, 20, 10], [40, 30, 40, 30]]
        expected_y = [[10, 20, 40], [40, 30, 20, 10]]
        test_plot.figure.multi_line.assert_called_once_with(expected_x, expected_y, **STYLE_KWARGS)

    def test__plot_lines__verify_empty(self):
        """ Verify `_plot_lines` calls methods with expected arguments when given empty shape.
        """
        test_plot = self.setup_plot()
        with patch.object(test_plot, "logger", Mock(spec=logging)) as mock_logger:
            test_plot._plot_lines(wkt.loads("LINESTRING EMPTY"), **STYLE_KWARGS)
            mock_logger.info.assert_called_once_with("Given shape is empty, returning.")
            test_plot.figure.line.assert_not_called()
            test_plot.figure.multi_line.assert_not_called()

    def test__plot_lines__verify_unexpected_shape_raises_TypeError(self):
        """ Verify `_plot_lines` raises TypeError when given unexpected shape.
        """
        test_plot = self.setup_plot()
        with self.assertRaises(TypeError) as e:
            test_plot._plot_lines(wkt.loads("POLYGON ((1 0, 1 1, 0 1, 0 0, 1 0))"), **STYLE_KWARGS)
        self.assertIn("Given `shape` argument is of an unexpected type [Polygon]", e.exception.args)

    # --- _plot_polys tests ---
    def test__poly_polys__verify_polygon(self):
        """ Verify `_plot_polys` calls methods with expected arguments when given `Polygon` shape.
        """
        test_plot = self.setup_plot()
        coords = ([[30.0, 40.0, 20.0, 10.0]], [[10.0, 40.0, 40.0, 20.0]])
        with patch.object(test_plot, "_get_poly_coordinates") as mock_coords:
            mock_coords.return_value = coords
            test_plot._plot_polys(wkt.loads("POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))"), **STYLE_KWARGS)
            test_plot.figure.multi_polygons.assert_called_once_with([[coords[0]]], [[coords[1]]], **STYLE_KWARGS)
    
    def test__poly_polys__verify_multipolygon(self):
        """ Verify `_plot_polys` calls methods with expected arguments when given `MultiPolygon` shape.
        """
        test_plot = self.setup_plot()
        coords = ([[30.0, 45.0, 10.0], [15.0, 40.0, 10.0, 5.0]], [[20.0, 40.0, 40.0], [5.0, 10.0, 20.0, 10.0]])
        with patch.object(test_plot, "_get_poly_coordinates") as mock_coords:
            mock_coords.return_value = coords
            test_plot._plot_polys(wkt.loads("MULTIPOLYGON (((30 20, 45 40, 10 40, 30 20)), ((15 5, 40 10, 10 20, 5 10, 15 5)))"), **STYLE_KWARGS)
            test_plot.figure.multi_polygons.assert_called_once_with([[coords[0]]], [[coords[1]]], **STYLE_KWARGS)
    
    def test__plot_polys__verify_empty(self):
        """ Verify `_plot_polys` calls methods with expected arguments when given empty shape.
        """
        test_plot = self.setup_plot()
        with patch.object(test_plot, "logger", Mock(spec=logging)) as mock_logger:
            test_plot._plot_polys(wkt.loads("POLYGON EMPTY"), **STYLE_KWARGS)
            mock_logger.info.assert_called_once_with("Given shape is empty, returning.")
            test_plot.figure.multi_polygons.assert_not_called()
    
    def test__poly_polys__verify_unexpected_shape_raises_TypeError(self):
        """ Verify `_plot_polys` raises TypeError when given unexpected shape.
        """
        test_plot = self.setup_plot()
        with self.assertRaises(TypeError) as e:
            test_plot._plot_polys(wkt.loads("LINEARRING (10 20, 20 25, 35 50, 10 20)"), **STYLE_KWARGS)
        self.assertIn("Given `shape` argument is of an unexpected type [LinearRing]", e.exception.args)

    # --- _get_poly_coordinates tests ---
    def test__get_poly_coordinates__verify_output_solid_polygon(self):
        test_plot = self.setup_plot()
        x, y = test_plot._get_poly_coordinates(wkt.loads("POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))"))
        self.assertEqual(x, [ [30.0, 40.0, 20.0, 10.0] ])
        self.assertEqual(y, [ [10.0, 40.0, 40.0, 20.0] ])

    def test__get_poly_coordinates__verify_output_hollow_polygon(self):
        test_plot = self.setup_plot()
        x, y = test_plot._get_poly_coordinates(wkt.loads("POLYGON ((35 10, 45 45, 15 40, 10 20, 35 10), (20 30, 35 35, 30 20, 20 30))"))
        self.assertEqual(x, [ [35.0, 45.0, 15.0, 10.0], [20.0, 35.0, 30.0] ])
        self.assertEqual(y, [ [10.0, 45.0, 40.0, 20.0], [30.0, 35.0, 20.0] ])
    
    def test__get_poly_coordinates__verify_output_solid_multipolygon(self):
        test_plot = self.setup_plot()
        x, y = test_plot._get_poly_coordinates(wkt.loads("MULTIPOLYGON (((30 20, 45 40, 10 40, 30 20)), ((15 5, 40 10, 10 20, 5 10, 15 5)))"))
        self.assertEqual(x, [ [30.0, 45.0, 10.0], [15.0, 40.0, 10.0, 5.0] ])
        self.assertEqual(y, [ [20.0, 40.0, 40.0], [5.0, 10.0, 20.0, 10.0] ])

    def test__get_poly_coordinates__verify_output_hollow_multipolygon(self):
        test_plot = self.setup_plot()
        x, y = test_plot._get_poly_coordinates(wkt.loads("MULTIPOLYGON (((40 40, 20 45, 45 30, 40 40)), ((20 35, 10 30, 10 10, 30 5, 45 20, 20 35), (30 20, 20 15, 20 25, 30 20)))"))
        self.assertEqual(x, [ [40.0, 20.0, 45.0], [20.0, 10.0, 10.0, 30.0, 45.0], [30.0, 20.0, 20.0] ])
        self.assertEqual(y, [ [40.0, 45.0, 30.0], [35.0, 30.0, 10.0,  5.0, 20.0], [20.0, 15.0, 25.0] ])
    
    def test__get_poly_coordinates_verify_unexpected_shape_raises_TypeError(self):
        """ Verify `_get_poly_coordinates` raises TypeError when given unexpected shape.
        """
        test_plot = self.setup_plot()
        with self.assertRaises(TypeError) as e:
            test_plot._get_poly_coordinates(wkt.loads("LINEARRING (10 20, 20 25, 35 50, 10 20)"))
        self.assertIn("Given `shape` argument is of an unexpected type [LinearRing]", e.exception.args)


if __name__ == "__main__":
    unittest.main()
