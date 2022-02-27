import string
import tempfile
import unittest

from bokeh.plotting import figure
from shapely import wkt
from unittest.mock import Mock, patch
from wktplot import WKTPlot


PLOT_TITLE = "test_1234"
STYLE_KWARGS = {"color": "MidnightBlue", "line_width": 3.0}


class InternalFunctionTests(unittest.TestCase):

    # --- _plot_points tests ---
    @patch("wktplot.wktplot.figure", Mock(spec_set=figure))
    def test__plot_points__verify_point(self):
        """ Verify `_plot_points` calls methods with expected arguments when given `Point` shape.
        """

        shape = wkt.loads("POINT (30 10)")
        expected_x = [30]
        expected_y = [10]
        with tempfile.TemporaryDirectory() as temp_dir:
            plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
            plot._plot_points(shape, **STYLE_KWARGS)
            plot.figure.circle.assert_called_once_with(expected_x, expected_y, **STYLE_KWARGS)

    @patch("wktplot.wktplot.figure", Mock(spec_set=figure))
    def test__plot_points__verify_multipoint(self):
        """ Verify `_plot_points` calls methods with expected arguments when given `MultiPoint` shape.
        """

        shape = wkt.loads("MULTIPOINT ((10 40), (40 30), (20 20), (30 10))")
        expected_x = [10, 40, 20, 30]
        expected_y = [40, 30, 20, 10]
        with tempfile.TemporaryDirectory() as temp_dir:
            plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
            plot._plot_points(shape, **STYLE_KWARGS)
            plot.figure.circle.assert_called_once_with(expected_x, expected_y, **STYLE_KWARGS)

    @patch("wktplot.wktplot.figure", Mock(spec_set=figure))
    def test__plot_points__verify_empty(self):
        """ Verify `_plot_points` calls methods with expected arguments when given empty shape.
        """

        empty_shape = wkt.loads("POINT EMPTY")
        with tempfile.TemporaryDirectory() as temp_dir:
            plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
            plot._plot_points(empty_shape, **STYLE_KWARGS)
            plot.figure.circle.assert_not_called()

    def test__plot_points__verify_unexpected_shape_raises_TypeError(self):
        """ Verify `_plot_points` raises TypeError when given unexpected shape.
        """

        invalid_shape = wkt.loads("POLYGON ((1 0, 1 1, 0 1, 0 0, 1 0))")
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(TypeError):
                plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
                plot._plot_points(invalid_shape, **STYLE_KWARGS)

    # --- _plot_lines tests ---
    @patch("wktplot.wktplot.figure", Mock(spec_set=figure))
    def test__plot_lines__verify_linestring(self):
        """ Verify `_plot_lines` calls methods with expected arguments when given `LineString` shape.
        """

        shape = wkt.loads("LINESTRING (30 10, 10 30, 40 40)")
        expected_x = [30, 10, 40]
        expected_y = [10, 30, 40]
        with tempfile.TemporaryDirectory() as temp_dir:
            plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
            plot._plot_lines(shape, **STYLE_KWARGS)
            plot.figure.line.assert_called_once_with(expected_x, expected_y, **STYLE_KWARGS)

    @patch("wktplot.wktplot.figure", Mock(spec_set=figure))
    def test__plot_lines__verify_linear_ring(self):
        """ Verify `_plot_lines` calls methods with expected arguments when given `LinearRing` shape.
        """

        shape = wkt.loads("LINEARRING (10 20, 20 25, 35 50, 10 20)")
        expected_x = [10, 20, 35, 10]
        expected_y = [20, 25, 50, 20]
        with tempfile.TemporaryDirectory() as temp_dir:
            plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
            plot._plot_lines(shape, **STYLE_KWARGS)
            plot.figure.line.assert_called_once_with(expected_x, expected_y, **STYLE_KWARGS)

    @patch("wktplot.wktplot.figure", Mock(spec_set=figure))
    def test__plot_lines__verify_multilinestring(self):
        """ Verify `_plot_lines` calls methods with expected arguments when given `MultiLineString` shape.
        """

        shape = wkt.loads("MULTILINESTRING ((10 10, 20 20, 10 40), (40 40, 30 30, 40 20, 30 10))")
        expected_x = [ [10, 20, 10], [40, 30, 40, 30] ]
        expected_y = [ [10, 20, 40], [40, 30, 20, 10] ]
        with tempfile.TemporaryDirectory() as temp_dir:
            plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
            plot._plot_lines(shape, **STYLE_KWARGS)
            plot.figure.multi_line.assert_called_once_with(expected_x, expected_y, **STYLE_KWARGS)

    @patch("wktplot.wktplot.figure", Mock(spec_set=figure))
    def test__plot_lines__verify_empty(self):
        """ Verify `_plot_lines` calls methods with expected arguments when given empty shape.
        """

        empty_shape = wkt.loads("LINESTRING EMPTY")
        with tempfile.TemporaryDirectory() as temp_dir:
            plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
            plot._plot_lines(empty_shape, **STYLE_KWARGS)
            plot.figure.line.assert_not_called()
            plot.figure.multi_line.assert_not_called()

    def test__plot_lines__verify_unexpected_shape_raises_TypeError(self):
        """ Verify `_plot_lines` raises TypeError when given unexpected shape.
        """

        invalid_shape = wkt.loads("POLYGON ((1 0, 1 1, 0 1, 0 0, 1 0))")
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(TypeError):
                plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
                plot._plot_lines(invalid_shape, **STYLE_KWARGS)

    # --- _plot_polys tests ---
    @patch("wktplot.wktplot.figure", Mock(spec_set=figure))
    def test__poly_polys__verify_polygon(self):
        """ Verify `_plot_polys` calls methods with expected arguments when given `Polygon` shape.
        """

        shape = wkt.loads("POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))")
        expected_x = [ [30.0, 40.0, 20.0, 10.0] ]
        expected_y = [ [10.0, 40.0, 40.0, 20.0] ]
        with tempfile.TemporaryDirectory() as temp_dir:
            plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
            with patch.object(plot, "_get_poly_coordinates", Mock(return_value=(expected_x, expected_y))):
                plot._plot_polys(shape, **STYLE_KWARGS)
                plot.figure.multi_polygons.assert_called_once_with([[expected_x]], [[expected_y]], **STYLE_KWARGS)

    @patch("wktplot.wktplot.figure", Mock(spec_set=figure))
    def test__poly_polys__verify_multipolygon(self):
        """ Verify `_plot_polys` calls methods with expected arguments when given `MultiPolygon` shape.
        """

        shape = wkt.loads("MULTIPOLYGON (((30 20, 45 40, 10 40, 30 20)), ((15 5, 40 10, 10 20, 5 10, 15 5)))")
        expected_x = [ [30.0, 45.0, 10.0], [15.0, 40.0, 10.0, 5.0] ]
        expected_y = [ [20.0, 40.0, 40.0], [5.0, 10.0, 20.0, 10.0] ]
        with tempfile.TemporaryDirectory() as temp_dir:
            plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
            with patch.object(plot, "_get_poly_coordinates", Mock(return_value=(expected_x, expected_y))):
                plot._plot_polys(shape, **STYLE_KWARGS)
                plot.figure.multi_polygons.assert_called_once_with([[expected_x]], [[expected_y]], **STYLE_KWARGS)

    @patch("wktplot.wktplot.figure", Mock(spec_set=figure))
    def test__plot_polys__verify_empty(self):
        """ Verify `_plot_polys` calls methods with expected arguments when given empty shape.
        """

        empty_shape = wkt.loads("POLYGON EMPTY")
        with tempfile.TemporaryDirectory() as temp_dir:
            plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
            plot._plot_polys(empty_shape, **STYLE_KWARGS)
            plot.figure.multi_polygons.assert_not_called()

    def test__poly_polys__verify_unexpected_shape_raises_TypeError(self):
        """ Verify `_plot_polys` raises TypeError when given unexpected shape.
        """

        invalid_shape = wkt.loads("LINEARRING (10 20, 20 25, 35 50, 10 20)")
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(TypeError):
                plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
                plot._plot_polys(invalid_shape, **STYLE_KWARGS)

    # --- _get_poly_coordinates tests ---
    def test__get_poly_coordinates__verify_output_solid_polygon(self):
        """ Verify `_get_poly_coordinates` returns expected values when given solid shape.
        """

        shape = wkt.loads("POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))")
        expected_x = [ [30.0, 40.0, 20.0, 10.0] ]
        expected_y = [ [10.0, 40.0, 40.0, 20.0] ]
        with tempfile.TemporaryDirectory() as temp_dir:
            plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
            x, y = plot._get_poly_coordinates(shape)
            self.assertEqual(x, expected_x)
            self.assertEqual(y, expected_y)

    def test__get_poly_coordinates__verify_output_hollow_polygon(self):
        """ Verify `_get_poly_coordinates` returns expected values when given hollow shape.
        """

        shape = wkt.loads("POLYGON ((35 10, 45 45, 15 40, 10 20, 35 10), (20 30, 35 35, 30 20, 20 30))")
        expected_x = [ [35.0, 45.0, 15.0, 10.0], [20.0, 35.0, 30.0] ]
        expected_y = [ [10.0, 45.0, 40.0, 20.0], [30.0, 35.0, 20.0] ]
        with tempfile.TemporaryDirectory() as temp_dir:
            plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
            x, y = plot._get_poly_coordinates(shape)
            self.assertEqual(x, expected_x)
            self.assertEqual(y, expected_y)

    def test__get_poly_coordinates__verify_output_solid_multipolygon(self):
        """ Verify `_get_poly_coordinates` returns expected values when multiple solid shapes.
        """

        shape = wkt.loads("MULTIPOLYGON (((30 20, 45 40, 10 40, 30 20)), ((15 5, 40 10, 10 20, 5 10, 15 5)))")
        expected_x = [ [30.0, 45.0, 10.0], [15.0, 40.0, 10.0, 5.0] ]
        expected_y = [ [20.0, 40.0, 40.0], [5.0, 10.0, 20.0, 10.0] ]
        with tempfile.TemporaryDirectory() as temp_dir:
            plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
            x, y = plot._get_poly_coordinates(shape)
            self.assertEqual(x, expected_x)
            self.assertEqual(y, expected_y)

    def test__get_poly_coordinates__verify_output_hollow_multipolygon(self):
        """ Verify `_get_poly_coordinates` returns expected values when multiple hollow shapes.
        """

        shape = wkt.loads("MULTIPOLYGON (((40 40, 20 45, 45 30, 40 40)), ((20 35, 10 30, 10 10, 30 5, 45 20, 20 35), (30 20, 20 15, 20 25, 30 20)))")  # noqa: E501
        expected_x = [ [40.0, 20.0, 45.0], [20.0, 10.0, 10.0, 30.0, 45.0], [30.0, 20.0, 20.0] ]
        expected_y = [ [40.0, 45.0, 30.0], [35.0, 30.0, 10.0,  5.0, 20.0], [20.0, 15.0, 25.0] ]
        with tempfile.TemporaryDirectory() as temp_dir:
            plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
            x, y = plot._get_poly_coordinates(shape)
            self.assertEqual(x, expected_x)
            self.assertEqual(y, expected_y)

    def test__get_poly_coordinates__verify_unexpected_shape_raises_TypeError(self):
        """ Verify `_get_poly_coordinates` raises TypeError when given unexpected shape.
        """

        invalid_shape = wkt.loads("LINEARRING (10 20, 20 25, 35 50, 10 20)")
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(TypeError):
                plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
                plot._get_poly_coordinates(invalid_shape)

    def test__remove_symbols__verify_return_values(self):
        """ Verify `_remove_symbols` returns expected output.
        """

        i_o = [
            ("hello", "hello"),
            ("hello 123", "hello_123"),
            ("wowzers . 456789", "wowzers_456789"),
            ("123 yep ok", "123_yep_ok"),
            ("okeey !@#$%^&*()[]\\|;'\"_<>?`~", "okeey")
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            dummy = WKTPlot(title="test", save_dir=temp_dir)
            for i, o in i_o:
                self.assertEqual(dummy._remove_symbols(i), o)

    def test__get_random_string__verify_return_length_and_is_alpha_numeric(self):
        """ Verify '_get_random_string'
        """

        valid_chars = set(string.ascii_letters + string.digits)
        with tempfile.TemporaryDirectory() as temp_dir:
            dummy = WKTPlot(title="test", save_dir=temp_dir)
            for v in [3, 7, 11]:
                text = dummy._get_random_string(string_length=v)
                self.assertEqual(len(text), v)
                self.assertTrue(set(text).issubset(valid_chars))

if __name__ == "__main__":
    unittest.main()
