from shapely import wkt
from unittest.mock import Mock, patch
from wktplot.wkt_plot import WKTPlot

import logging
import unittest

PLOT_TITLE = "test_1234"
PLOT_SAVE_DIR = "/tmp/mock_me_up_scotty"

class InternalFunctionTests(unittest.TestCase):

    @patch("wktplot.wkt_plot.Path")
    @patch("wktplot.wkt_plot.output_file", Mock())
    @patch("wktplot.wkt_plot.figure", Mock())
    def setup_plot(self, mock_path):
        mock_path.is_dir.return_value = True
        return WKTPlot(title=PLOT_TITLE, save_dir=PLOT_SAVE_DIR)

    @patch("wktplot.wkt_plot.figure", Mock())
    def test__plot_points__verify_methods_called_point(self):
        test_plot = self.setup_plot()
        test_plot.figure.circle.reset_mock()
        test_plot._plot_points(wkt.loads("POINT (30 10)"))
        expected_x = [30]
        expected_y = [10]
        test_plot.figure.circle.assert_called_once_with(expected_x, expected_y, line_width=3)

    @patch("wktplot.wkt_plot.figure", Mock())
    def test__plot_points__verify_methods_called_multipoints(self):
        test_plot = self.setup_plot()
        test_plot.figure.circle.reset_mock()
        test_plot._plot_points(wkt.loads("MULTIPOINT ((10 40), (40 30), (20 20), (30 10))"))
        expected_x = [10, 40, 20, 30]
        expected_y = [40, 30, 20, 10]
        test_plot.figure.circle.assert_called_once_with(expected_x, expected_y, line_width=3)
    
    @patch("wktplot.wkt_plot.figure", Mock())
    def test__plot_points__verify_methods_called_empty(self):
        test_plot = self.setup_plot()
        with patch.object(test_plot, "logger", Mock(spec=logging)) as mock_logger:
            test_plot._plot_points(wkt.loads("POINT EMPTY"))
            mock_logger.info.assert_called_once_with("Given shape is empty, returning.")
            test_plot.figure.circle.assert_not_called()

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
    



if __name__ == "__main__":
    unittest.main()
        
