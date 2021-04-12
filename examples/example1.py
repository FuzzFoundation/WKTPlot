from wktplot.wkt_plot import WKTPlot
from shapely import wkt

s = wkt.loads("LINESTRING (30 10, 10 30, 40 40)")
p = WKTPlot("test")
p.plot_line(s, "red")
p.save("test.html")
