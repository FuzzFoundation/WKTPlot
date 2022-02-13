from pathlib import Path
from wktplot import WKTPlot


with WKTPlot(title="example2", save_dir=Path(__file__).parent, save_on_exit=True) as plot:
    plot.add_shape(
        "MULTILINESTRING ((10 10, 20 20, 10 40), (40 40, 30 30, 40 20, 30 10))",
        **{
            "line_width": 10,
            "line_color": "rebeccapurple",
        }
    )
