# WKTPlot
Plot well-known-text strings and shapely geometries with Bokeh!

## Badges
[![codecov](https://codecov.io/gh/FuzzFoundation/WKTPlot/branch/main/graph/badge.svg?token=E1BJVWQLRE)](https://codecov.io/gh/FuzzFoundation/WKTPlot)

## Installation
```
pip install wktplot
```

## Usage
``` python
from shapely.geometry import Polygon
from wktplot import WKTPlot

# Create plot object
plot = WKTPlot(title="My first plot!", save_dir="/path/to/directory")

# Define shapes either through well-known-text (WKT) string, or shapely object
shape_1 = "POINT (30 10)"
shape_2 = Polygon([[30, 10], [40, 40], [20, 40], [10, 20], [30, 10]])

# Add shapes to the plot
plot.add_shape(shape_1, fill_color="green", line_width=3)
plot.add_shape(shape_2, fill_color="cyan", fill_alpha=0.7)

# Save the plot to disk [/path/to/directory/my_first_plot.html]
plot.save()
```
WKTPlot supports majority of shapely objects including:
* Point
* MultiPoint
* LineString
* MultiLineString
* LinearRing
* Polygon
* MultiPolygon
* GeometryCollection

Example for plotting from shapefile. Shapefile is of California's county boundaries from [here](https://data.ca.gov/dataset/ca-geographic-boundaries).
```python
from random import randrange
from shapely.geometry import Polygon
from wktplot.wkt_plot import WKTPlot

import shapefile  # pyshp module

def get_rand_color():
    return f"#{randrange(0, 0xffffff):0>6x}"

plot = WKTPlot(title="California Counties", save_dir="~/scratch")
with shapefile.Reader("~/scratch/CA_Counties_TIGER2016.shp") as shp:
    for shape in shp.shapes():
        p = Polygon(shape.points)
        plot.add_shape(p, fill_color=get_rand_color())
plot.save()
```
Which will result in this output:
![CaliforniaCounties](docs/ca_counties.png)

## Additional Info
WKTPlot supports Bokeh's stylization parameters for customizing the look of added elements. See this guide for more info: https://docs.bokeh.org/en/latest/docs/user_guide/styling.html

## Future Plans
* Add native support for visualizing GeoDataframes and shapefiles.
* Make web view more interactive.
