from pathlib import Path
from unittest.mock import MagicMock
from wktplot.plots.standard import WKTPlot

import tempfile
import pytest

PLOT_TITLE = "Michael Plot ABC123"
PLOT_FILE = "michael_plot_abc123.html"
STYLE_KWARGS = {"color": "MidnightBlue", "line_width": 3.0}


@pytest.fixture()
def mock_bokeh(mocker) -> MagicMock:
    mock_bokeh: MagicMock = mocker.patch("wktplot.plots.standard.plt")
    return mock_bokeh


@pytest.fixture()
def temp_dir() -> str:
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture()
def mock_plot(mock_bokeh: MagicMock, temp_dir: str) -> WKTPlot:
    plot = WKTPlot(
        title=PLOT_TITLE,
        save_dir=temp_dir,
        **STYLE_KWARGS,
    )
    plot.mapper = MagicMock()
    yield plot


@pytest.fixture()
def mock_plot_without_save_dir(mock_bokeh: MagicMock) -> WKTPlot:
    plot = WKTPlot(
        title=PLOT_TITLE,
        **STYLE_KWARGS,
    )
    plot.mapper = MagicMock()
    yield plot


class TestConstructor:

    def test_when_given_invalid_save_dir_raises_OSError(self) -> None:

        invalid_dirs = [
            -1,
            0.01,
            False,
            b"ok",
            "not_a_directory",
            [0, 1],
            {"x": 1},
            set("abc"),
            2-3j,
        ]

        for save_dir in invalid_dirs:
            with pytest.raises(OSError):
                WKTPlot(save_dir=save_dir)

    def test_when_given_invalid_title_raises_ValueError(self) -> None:

        invalid_titles = [
            1,
            0.0001,
            True,
            b"wow",
            [1, 2, 3],
            {"a": 1},
            set("abc"),
            1+5j,
        ]

        for title in invalid_titles:
            with pytest.raises(ValueError):
                WKTPlot(title=title)

    def test_when_given_valid_arguments_figure_class_var_set(
        self,
        mock_bokeh: MagicMock,
        temp_dir: str,
        mock_plot: WKTPlot,
    ) -> None:

        expected_path = Path(temp_dir) / PLOT_FILE
        expected_kwargs = {
            **STYLE_KWARGS,
            **mock_plot.default_figure_style_kwargs,
        }
        mock_bokeh.output_file.assert_called_once_with(
            filename=expected_path,
            title=PLOT_TITLE,
            mode="inline",
        )
        mock_bokeh.figure.assert_called_once_with(
            title=PLOT_TITLE,
            **expected_kwargs,
        )
        assert mock_plot.figure.toolbar.autohide == True
    
    def test_when_not_given_save_dir_bokeh_output_file_not_set(
        self,
        mock_bokeh: MagicMock,
        mock_plot_without_save_dir: WKTPlot,
    ) -> None:

        expected_kwargs = {
            **STYLE_KWARGS,
            **mock_plot_without_save_dir.default_figure_style_kwargs,
        }
        mock_bokeh.output_file.assert_not_called()
        mock_bokeh.figure.assert_called_once_with(
            title=PLOT_TITLE,
            **expected_kwargs,
        )


class TestSave:

    def test_verify_plot_saved(
        self,
        mock_bokeh: MagicMock,
        mock_plot: WKTPlot,
    ) -> None:

        mock_plot.save()
        mock_bokeh.save.assert_called_once_with(mock_plot.figure)

class TestShow:

    def test_verify_plot_shown(
        self,
        mock_bokeh: MagicMock,
        mock_plot: WKTPlot,
    ) -> None:

        mock_plot.show()
        mock_bokeh.show.assert_called_once_with(mock_plot.figure)

class TestAddShape:

    def test_verify_mapper_called(self, mock_plot: WKTPlot) -> None:

        mock_shape = MagicMock()
        mock_plot.add_shape(mock_shape, **STYLE_KWARGS)
        mock_plot.mapper.add_shape.assert_called_once_with(
            mock_plot.figure,
            mock_shape,
            **STYLE_KWARGS,
        )
