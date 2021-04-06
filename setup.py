from setuptools import find_packages, setup
from wktplot import __version__

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="wktplot",
    version=__version__,
    license="MIT",
    author="Michael Simpson, Gerald Sornsen",
    author_email="mikeysimpson4@gmail.com, gerald@sornsen.io",
    description="Python wrapper for visualiation of shapely geometries.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/FuzzFoundation/WKTPlot",
    packages=find_packages(),
    install_requires=[
        "descartes>=1.1.0",
        "Shapely>=1.7.1"
    ],
    python_requires=">=3.7",
    classifiers=[
      "License :: OSI Approved :: MIT License",
      "Programming Language :: Python",
      "Programming Language :: Python :: 3.7",
      "Programming Language :: Python :: 3.8",
      "Programming Language :: Python :: 3.9",
      "Natural Language :: English",
      "Operating System :: OS Independent",
      "Development Status :: 5 - Production/Stable",
      "Intended Audience :: Developers",
      "Topic :: Software Development :: Libraries"],
    keywords="shapely matplotlib GeoDataframes geometries",
    include_package_data=True,
    platforms="Posix; MacOS X; Windows"
)
