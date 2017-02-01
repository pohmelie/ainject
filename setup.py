import setuptools


config = setuptools.config.read_configuration("setup.cfg")
setuptools.setup(**config["metadata"])
