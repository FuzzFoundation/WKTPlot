# WKTPlot

Utility for plotting shapely geometries and WKTs

## Badges

[![CircleCI](https://circleci.com/gh/FuzzFoundation/WKTPlot.svg?style=shield)](https://circleci.com/gh/FuzzFoundation/WKTPlot)

## Usage

Example:

```python
from wkt_plot import WKTPLOT

a = Polygon(...)
b = MultiPolygon(...)
c = LineString(...)
d = MultiLineString(...)
e = "LINESTRING (30 10, 10 30, 40 40)"

plot = WKTPLOT("path/to/save/directory")
plot.add_shape(a, fill_color="crimson", name="A Poly")
plot.add_shape(c, stroke_color="dimgray")
plot.add_shape(e, "cornflowerblue")
plot.save(plot_name="A with C with E")
plot.clear()

plot.add_shapes([
    (b, "magenta"),
    (c, "turquoise"),
    (d, "forestgreen")
]).save("BCD").clear()
```
