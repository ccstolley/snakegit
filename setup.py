#!/usr/bin/env python

import ConfigParser
import setuptools

config = ConfigParser.RawConfigParser()
config.read("snake.cfg")

scripts = ["{0}={1}".format(key, config.get('commands', key)) for key in config.options("commands")]


with open("requirements.txt", 'r') as f:
	requires = [req.strip() for req in f.readlines()]

setuptools.setup(
		name=config.get("release", "name"),
		version=config.get("release", "version"),
		description=config.get("release", "description"),
		package_dir={"":"src"},
		packages=setuptools.find_packages("src"),
#		install_requires=requires,
		package_data = {
			"snakes": ["nyan"]
			},
		entry_points = {
			"snake_scripts": scripts,
			"console_scripts": scripts 
			}
		)

