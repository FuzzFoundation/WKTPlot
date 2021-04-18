from pathlib import Path
from wktplot.wkt_plot import WKTPlot

# https://docs.bokeh.org/en/latest/docs/user_guide/plotting.html

shapes = {
    # Well-known text strings from Wikipedia: https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry
    "SinglePoint": "POINT (30 10)",
    "LineString": "LINESTRING (30 10, 10 30, 40 40)",
    "MultiPoint1": "MULTIPOINT ((10 40), (40 30), (20 20), (30 10))",
    "LinearRing": "LINEARRING (10 20, 20 25, 35 50, 10 20)",
    "MultiPoint2": "MULTIPOINT (10 40, 40 30, 20 20, 30 10)",
    "MultiLineString": "MULTILINESTRING ((10 10, 20 20, 10 40), (40 40, 30 30, 40 20, 30 10))",
    "SolidPolygon": "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))",
    "HollowPolygon": "POLYGON ((35 10, 45 45, 15 40, 10 20, 35 10), (20 30, 35 35, 30 20, 20 30))",
    "MultiPolygonSolid": "MULTIPOLYGON (((30 20, 45 40, 10 40, 30 20)), ((15 5, 40 10, 10 20, 5 10, 15 5)))",
    "MultiPolygonHollow": "MULTIPOLYGON (((40 40, 20 45, 45 30, 40 40)), ((20 35, 10 30, 10 10, 30 5, 45 20, 20 35), (30 20, 20 15, 20 25, 30 20)))",
    "EmptyCollection": "GEOMETRYCOLLECTION EMPTY",
    "FullCollection": "GEOMETRYCOLLECTION (POINT (40 10), LINESTRING (10 10, 20 20, 10 40), POLYGON ((40 40, 20 45, 45 30, 40 40)))"
}

def test1():
    for name, shape in shapes.items():
        try:
            print(name)
            p = WKTPlot(title=f"test_{name}", save_dir=Path(__file__).parent)
            p.add_shape(shape)
            p.save()
            del p
        except Exception as e:
            print(f"Shape: {name} not working. \n\t{e}")

test1()
