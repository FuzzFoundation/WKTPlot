# WKTPlot
Wrapper around the [Bokeh](https://github.com/bokeh/bokeh) library for plotting well-known-text strings and shapely geometries!

## Badges
[![PyPi Python Versions](https://img.shields.io/pypi/pyversions/wktplot.svg)](https://pypi.org/project/wktplot/)
[![codecov](https://codecov.io/gh/FuzzFoundation/WKTPlot/branch/main/graph/badge.svg?token=E1BJVWQLRE)](https://codecov.io/gh/FuzzFoundation/WKTPlot)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/19fe4574645d492e8677c4b06152dd9d)](https://www.codacy.com/gh/FuzzFoundation/WKTPlot/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=FuzzFoundation/WKTPlot&amp;utm_campaign=Badge_Grade)

## Installation
```
pip install wktplot
```

## Description
The [well-known-text](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) standard is very common for working with and representing geospatial data, however it is painful to visualize them programatically. The [Shapely](https://github.com/shapely/shapely) library  extends the functionality of the well-known-text standard with a rich assortment of geometry objects and operations, but it doesn't make it any easier to visualize.

WKTPlot is a library provides an easy-to-use API for visualizing well-known-text strings and shapely objects programatically. This library wraps around the [Bokeh](https://github.com/bokeh/bokeh) library, which is a powerful plotting library for generating interactive visualizations. Bokeh also provides a rich assortment of [stylizing options](https://docs.bokeh.org/en/latest/docs/user_guide/styling.html) which are all usable through WKTPlot's `add_shape` method.

## Basic Usage
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

### Supported datatypes
WKTPlot supports majority of shapely objects including:
* Point
* MultiPoint
* LineString
* MultiLineString
* LinearRing
* Polygon
* MultiPolygon
* GeometryCollection

## Advanced Usage
Example for plotting from shapefile. Shapefile is of California's county boundaries from [here](https://data.ca.gov/dataset/ca-geographic-boundaries).
```python
import shapefile  # pyshp module

from random import randrange
from shapely.geometry import Polygon
from wktplot import WKTPlot

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
![CaliforniaCounties](https://i.imgur.com/YPQQlml.png)

## Future Plans
* Add native support for visualizing GeoDataframes and shapefiles.
* Make web view more interactive.
