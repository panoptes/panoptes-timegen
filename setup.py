from setuptools import setup

setup(
    name = "panoptes_timegen",
    version = "0.0.1",
    author = "Naga",
    author_email = "devarintinagasaiabhinay@gmail.com",
    description = ("A simple time-lapse generator for FITS files generated by Project PANOPTES"),
    license = "MIT",
    keywords = "timelapse generator",
    url = "",
    packages=['panoptes_timegen', 'tests'],
    install_requires = ['astropy','Click','colour_demosaicing','opencv-python'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)