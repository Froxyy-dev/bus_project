import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bus_project",
    version="0.0.1",
    author="Mateusz Winiarek",
    author_email="mw448557@students.mimuw.edu.pl",
    description="Data analysis in Python project for the third semester course.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Froxyy-dev/bus_project",
    packages=setuptools.find_packages(),
    install_requires=[
        'folium',
        'geojson',
        'geopy',
        'matplotlib',
        'numpy',
        'pandas',
        'scikit-learn-extra',
        'pytest',
        'setuptools',
        'shapely',
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    python_requires='>=3.6',
)
