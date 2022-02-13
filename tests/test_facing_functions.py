from bokeh.plotting import figure, output_file
from itertools import product
from pathlib import Path
from shapely import wkt
from shapely.geometry import GeometryCollection, LineString, Polygon, Point
from shapely.geometry.base import BaseGeometry
from unittest.mock import Mock, patch, DEFAULT
from wktplot import WKTPlot

import tempfile
import unittest

PLOT_TITLE = "Michael Plot ABC123"
PLOT_FILE = "michael_plot_abc123.html"
STYLE_KWARGS = {"color": "MidnightBlue", "line_width": 3.0}


class FakeShape(BaseGeometry):
    """ Fake shapely shape to test NotImplementedError unittests.
    """

    @property
    def is_empty(self):
        return False


class FacingFunctionsTests(unittest.TestCase):

    @patch("wktplot.wktplot.output_file", Mock(spec_set=output_file))
    @patch("wktplot.wktplot.figure", Mock(spec_set=figure))
    def test_constructor__verify_invalid_save_dir_raises_OSError(self):
        """ Verify `WKTPlot.__init__` raises OSError when given an invalid `save_dir` value.
        """

        invalid_dir = "blah blah blah"
        with self.assertRaises(OSError):
            WKTPlot(title=PLOT_TITLE, save_dir=invalid_dir)

    @patch("wktplot.wktplot.output_file", spec_set=output_file)
    @patch("wktplot.wktplot.figure", spec_set=figure)
    def test_constructor__verify_methods_called(self, mock_figure: Mock, mock_output: Mock):
        """ Verify `WKTPlot.__init__` calls methods with expected arguments.
        """

        with tempfile.TemporaryDirectory() as temp_dir:
            plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
            mock_output.assert_called_once()
            mock_figure.assert_called_once()
            self.assertEqual(plot.figure, mock_figure.return_value)
            self.assertTrue(plot.figure.toolbar.autohide)

    @patch("wktplot.wktplot.output_file", Mock(spec_set=output_file))
    @patch("wktplot.wktplot.figure", Mock(spec_set=figure))
    @patch("wktplot.wktplot.Utils")
    def test_constructor__verify_empty_title_gets_random_value(self, mock_utils: Mock):
        """ Verify random string is generated if no title is given to constructor.
        """

        with tempfile.TemporaryDirectory() as temp_dir:
            WKTPlot(save_dir=temp_dir)
        
        mock_utils.get_random_string.assert_called_once()
        
    @patch("wktplot.wktplot.output_file", Mock(spec_set=output_file))
    @patch("wktplot.wktplot.figure", Mock(spec_set=figure))
    def test_add_shape__verify_nonrecursive_methods_called(self):
        """ Verify `add_shape` calls expected internal methods when given certain non-recursive shapes.
        """

        shape_method_map = {
            "_plot_points": [
                "POINT (30 10)",
                "MULTIPOINT ((10 40), (40 30), (20 20), (30 10))",
            ],
            "_plot_lines": [
                "LINESTRING (30 10, 10 30, 40 40)",
                "LINEARRING (10 20, 20 25, 35 50, 10 20)",
                "MULTILINESTRING ((10 10, 20 20, 10 40), (40 40, 30 30, 40 20, 30 10))",
            ],
            "_plot_polys": [
                "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))",
                "MULTIPOLYGON (((30 20, 45 40, 10 40, 30 20)), ((15 5, 40 10, 10 20, 5 10, 15 5)))",
            ],
        }

        for internal_method in shape_method_map:
            for shape_wkt in shape_method_map[internal_method]:
                shape = wkt.loads(shape_wkt)
                with tempfile.TemporaryDirectory() as temp_dir:
                    plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
                    with patch.object(plot, internal_method) as mock_plot_method:
                        plot.add_shape(shape_wkt, **STYLE_KWARGS)
                        mock_plot_method.assert_called_once_with(shape, **STYLE_KWARGS)

    @patch("wktplot.wktplot.output_file", Mock(spec_set=output_file))
    @patch("wktplot.wktplot.figure", Mock(spec_set=figure))
    def test_add_shape__verify_recursive_calls_when_given_geometrycollection(self):
        """ Verify `add_shape` calls expected internal methods when given recursive shape.
        """

        point = Point(40, 10)
        line_string = LineString([[10, 10], [20, 20], [10, 40]])
        polygon = Polygon([[40, 40], [20, 45], [45, 30], [40, 40]])
        collection = GeometryCollection([point, line_string, polygon])

        with tempfile.TemporaryDirectory() as temp_dir:
            plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
            with patch.multiple(plot, _plot_points=DEFAULT, _plot_lines=DEFAULT, _plot_polys=DEFAULT) as mock_methods:
                plot.add_shape(collection, **STYLE_KWARGS)
                mock_methods["_plot_points"].assert_called_once_with(point, **STYLE_KWARGS)
                mock_methods["_plot_lines"].assert_called_once_with(line_string, **STYLE_KWARGS)
                mock_methods["_plot_polys"].assert_called_once_with(polygon, **STYLE_KWARGS)

    @patch("wktplot.wktplot.output_file", Mock(spec_set=output_file))
    @patch("wktplot.wktplot.figure", Mock(spec_set=figure))
    def test_add_shape_verify_unexpected_shape_raises_NotImplementedError(self):
        """ Verify `add_shape` raises `NotImplementedError` when given an unknown object.
        """

        fake_shape = FakeShape()
        with tempfile.TemporaryDirectory() as temp_dir:
            plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
            with self.assertRaises(NotImplementedError):
                plot.add_shape(fake_shape, **STYLE_KWARGS)

    @patch("wktplot.wktplot.output_file", Mock(spec_set=output_file))
    @patch("wktplot.wktplot.figure", Mock(spec_set=figure))
    def test_add_shape__verify_empty_shape_returns(self):
        """ Verify `add_shape` returns early when given an empty shape.
        """

        shape = Point()
        with tempfile.TemporaryDirectory() as temp_dir:
            plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
            with patch.multiple(plot, _plot_points=DEFAULT, _plot_lines=DEFAULT, _plot_polys=DEFAULT) as mock_methods:
                plot.add_shape(shape, **STYLE_KWARGS)
                mock_methods["_plot_points"].assert_not_called()
                mock_methods["_plot_lines"].assert_not_called()
                mock_methods["_plot_polys"].assert_not_called()

    @patch("wktplot.wktplot.output_file", Mock(spec_set=output_file))
    @patch("wktplot.wktplot.figure", Mock(spec_set=figure))
    @patch("wktplot.wktplot.save")
    def test_save__verify_methods_called(self, mock_save: Mock):
        """ Verify `save` method calls method with expected arguments.
        """

        with tempfile.TemporaryDirectory() as temp_dir:
            plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
            plot.save()
            mock_save.assert_called_once_with(plot.figure)

    @patch("wktplot.wktplot.output_file", Mock(spec_set=output_file))
    @patch("wktplot.wktplot.figure", Mock(spec_set=figure))
    @patch("wktplot.wktplot.show")
    def test_show__verify_methods_called(self, mock_show: Mock):
        """ Verify `show` method calls method with expected arguments.
        """

        with tempfile.TemporaryDirectory() as temp_dir:
            plot = WKTPlot(title=PLOT_TITLE, save_dir=temp_dir)
            plot.show()
            mock_show.assert_called_once_with(plot.figure)
    
    @patch("wktplot.wktplot.output_file", Mock(spec_set=output_file))
    @patch("wktplot.wktplot.figure", Mock(spec_set=figure))
    @patch("wktplot.wktplot.show")
    @patch("wktplot.wktplot.save")
    def test_context_manager__verify_on_exit_calls(self, mock_save: Mock, mock_show: Mock):
        """ Verify `__exit__` calls save and / or show methods.
        """

        with tempfile.TemporaryDirectory() as temp_dir:
            for save_bool, show_bool in product([False, True], repeat=2):
                mock_save.reset_mock()
                mock_show.reset_mock()

                with WKTPlot(title=PLOT_TITLE, save_dir=temp_dir, save_on_exit=save_bool, show_on_exit=show_bool):
                    pass

                if save_bool:
                    mock_save.assert_called_once()
                else:
                    mock_save.assert_not_called()
                
                if show_bool:
                    mock_show.assert_called_once()
                else:
                    mock_show.assert_not_called()


if __name__ == "__main__":
    unittest.main()
