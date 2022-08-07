from wktplot.plots.osm import OpenStreetMapsPlot

shape = "POLYGON ((35 10, 45 45, 15 40, 10 20, 35 10), (20 30, 35 35, 30 20, 20 30))"

plot = OpenStreetMapsPlot("Open Street Map Plot", save_dir="/path/to/directory")
plot.add_shape(shape, fill_alpha=0.5, fill_color="firebrick")
plot.save()
