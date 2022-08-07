from shapely.geometry import LineString
from wktplot import WKTPlot

# Create plot object
plot = WKTPlot(title="My first plot!", save_dir="/path/to/directory")

# Define shapes either through well-known-text (WKT) string, or shapely object
line_string = LineString([[45, 5], [30, -7], [40, 10]])
polygon = "POLYGON ((35 10, 45 45, 15 40, 10 20, 35 10),(20 30, 35 35, 30 20, 20 30))"
points = "MULTIPOINT (17 11, 13 0, 22 -5, 25 7)"

# Add shapes to the plot with style args
plot.add_shape(line_string, line_color="firebrick", line_alpha=0.5, line_width=20)
plot.add_shape(polygon, fill_color="#6495ED", fill_alpha=0.5)
plot.add_shape(points, fill_color=(50, 205, 50, 0.25), fill_alpha=0.7, size=30)

# Save plot to disk [/path/to/directory/my_first_plot.html]
plot.save()
