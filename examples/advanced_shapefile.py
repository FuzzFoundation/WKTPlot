import shapefile  # pyshp module

from bokeh.palettes import Magma6
from pathlib import Path
from random import choice
from shapely.geometry import Polygon
from wktplot.plots.osm import OpenStreetMapsPlot


COUNTIES_PATH = Path("/path/to/CA_Counties_TIGER2016.shp")

# Create plot and disable mercator calculation
# because data has already been projected
plot = OpenStreetMapsPlot(
    title="California Counties 2016",
    height=1000,
    width=1000,
    disable_mercator=True,
)

# Read shapefile data points from file
with shapefile.Reader(COUNTIES_PATH) as shp:
    for shape in shp.shapes():
        plot.add_shape(
            shape=Polygon(shape.points),
            fill_color=choice(Magma6),
            fill_alpha=0.75,
        )

# Save plot to disk [./california_counties_2016.html]
plot.save()