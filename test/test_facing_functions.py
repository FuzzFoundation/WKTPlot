from pathlib import Path
from shapely.geometry.base import BaseGeometry
from shapely import wkt
from unittest.mock import Mock, patch, DEFAULT
from wktplot.wkt_plot import WKTPlot

import unittest


PLOT_TITLE = "Michael Plot ABC123"
PLOT_SAVE_DIR = "/tmp/mock_me_up_scotty"
STYLE_KWARGS = {"color": "MidnightBlue", "line_width": 3.0}

class FakeShape(BaseGeometry):
    @property
    def is_empty(self):
        return False



class FacingFunctionsTests(unittest.TestCase):

    @patch("wktplot.wkt_plot.Path")
    @patch("wktplot.wkt_plot.output_file", Mock())
    @patch("wktplot.wkt_plot.figure", Mock())
    def setup_plot(self, mock_path):
        mock_path.is_dir.return_value = True
        plot = WKTPlot(title=PLOT_TITLE, save_dir=PLOT_SAVE_DIR)
        return plot
    
    def test_constructor__verify_invalid_save_dir_raises_OSError(self):
        with self.assertRaises(OSError) as e:
            WKTPlot(title=PLOT_TITLE, save_dir=PLOT_SAVE_DIR)
        self.assertIn(f"Given argument `save_dir` is not a directory. [{PLOT_SAVE_DIR}]", e.exception.args)

    @patch("wktplot.wkt_plot.Path", spec=Path)
    @patch("wktplot.wkt_plot.output_file")
    @patch("wktplot.wkt_plot.figure")
    def test_constructor__verify_methods_called(self, mock_figure, mock_output, mock_path):
        expected_output_file = f"{PLOT_SAVE_DIR}/michael_plot_abc123.html"
        mock_path.return_value.is_dir.return_value = True
        mock_path.return_value.__truediv__.return_value = expected_output_file
        test_plot = WKTPlot(title=PLOT_TITLE, save_dir=PLOT_SAVE_DIR)
        mock_path.assert_called_once_with(PLOT_SAVE_DIR)
        mock_output.assert_called_once_with(expected_output_file, title=PLOT_TITLE, mode="inline")
        mock_figure.assert_called_once_with(title=PLOT_TITLE, x_axis_label="Longitude", y_axis_label="Latitude")
        self.assertTrue(test_plot.figure.toolbar.autohide)

    def test_add_shape__verify_nonrecursive_methods_called(self):
        shape_method_map = {
            "POINT (30 10)": "_plot_points",
            "MULTIPOINT ((10 40), (40 30), (20 20), (30 10))": "_plot_points",
            "LINESTRING (30 10, 10 30, 40 40)": "_plot_lines",
            "LINEARRING (10 20, 20 25, 35 50, 10 20)": "_plot_lines",
            "MULTILINESTRING ((10 10, 20 20, 10 40), (40 40, 30 30, 40 20, 30 10))": "_plot_lines",
            "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))": "_plot_polys",
            "MULTIPOLYGON (((30 20, 45 40, 10 40, 30 20)), ((15 5, 40 10, 10 20, 5 10, 15 5)))": "_plot_polys",
        }

        avail_methods = ["_plot_points", "_plot_lines", "_plot_polys"]

        for shape, expected_method in shape_method_map.items():
            test_plot = self.setup_plot()
            for method in avail_methods:
                setattr(test_plot, method, Mock(side_effect=Exception))
            with patch.object(test_plot, expected_method) as mock_plot_method:
                test_plot.add_shape(shape, **STYLE_KWARGS)
                mock_plot_method.assert_called_once_with(wkt.loads(shape), **STYLE_KWARGS)

    def test_add_shape__verify_recursive_calls_when_given_geometrycollection(self):
        shape = "GEOMETRYCOLLECTION (POINT (40 10), LINESTRING (10 10, 20 20, 10 40), POLYGON ((40 40, 20 45, 45 30, 40 40)))"
        test_plot = self.setup_plot()
        with patch.multiple(test_plot, _plot_points=DEFAULT, _plot_lines=DEFAULT, _plot_polys=DEFAULT) as mock_methods:
            test_plot.add_shape(shape, **STYLE_KWARGS)
            mock_methods["_plot_points"].assert_called_once_with(wkt.loads("POINT (40 10)"), **STYLE_KWARGS)
            mock_methods["_plot_lines"].assert_called_once_with(wkt.loads("LINESTRING (10 10, 20 20, 10 40)"), **STYLE_KWARGS)
            mock_methods["_plot_polys"].assert_called_once_with(wkt.loads("POLYGON ((40 40, 20 45, 45 30, 40 40))"), **STYLE_KWARGS)

    def test_add_shape_verify_unexpected_shape_raises_NotImplementedError(self):
        fake_shape = FakeShape()
        test_plot = self.setup_plot()
        with self.assertRaises(NotImplementedError) as e:
            test_plot.add_shape(fake_shape, **STYLE_KWARGS)
        self.assertIn("Given `shape` argument is of an unexpected type [FakeShape]", e.exception.args)
    
    def test_add_shape__verify_empty_shape_logs_message(self):
        shape = "POINT EMPTY"
        test_plot = self.setup_plot()
        with patch.object(test_plot, "logger") as mock_logger:
            mock_logger.info.reset_mock()
            test_plot.add_shape(shape, **STYLE_KWARGS)
            mock_logger.info.assert_called_once_with("Given shape is empty, returning.")
    
    @patch("wktplot.wkt_plot.save")
    def test_save__verify_methods_called(self, mock_save):
        test_plot = self.setup_plot()
        test_plot.save()
        mock_save.assert_called_once_with(test_plot.figure)
    
    @patch("wktplot.wkt_plot.show")
    def test_show__verify_methods_called(self, mock_show):
        test_plot = self.setup_plot()
        test_plot.show()
        mock_show.assert_called_once_with(test_plot.figure)


if __name__ == "__main__":
    unittest.main()
