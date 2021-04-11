# WKTPlot

Utility for plotting shapely geometries and WKTs

## Badges

[![CircleCI](https://circleci.com/gh/FuzzFoundation/WKTPlot.svg?style=shield)](https://circleci.com/gh/FuzzFoundation/WKTPlot)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/19fe4574645d492e8677c4b06152dd9d)](https://www.codacy.com/gh/FuzzFoundation/WKTPlot/dashboard?utm_source=github.com;utm_content=FuzzFoundation/WKTPlot&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/19fe4574645d492e8677c4b06152dd9d)](https://www.codacy.com/gh/FuzzFoundation/WKTPlot/dashboard?utm_source=github.com&utm_medium=referral&utm_content=FuzzFoundation/WKTPlot&utm_campaign=Badge_Coverage)

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
