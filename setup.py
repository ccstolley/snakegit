#!/usr/bin/env python

import ConfigParser
import setuptools

config = ConfigParser.RawConfigParser()
config.read("snake.cfg")


scripts = [
    "build =snakes.build:main",
    "bump =snakes.bump:main",
    "clean=snakes.clean:main",
    "test=snakes.test:main",
    "release=snakes.release:main",
    "sync_deps=snakes.update_deps:main",
    "snake=snakes.main:main",
    "nyan=snakes.nyan:main",
    "config=snakes.config:main",
    "update=snakes.update:main",
    "deps=snakes.deps:main",
    "lint=snakes.lint:main",
    "pullreq=snakes.pullreq:main",
    "init = snakes.init_project:main",
    "exec = snakes.execute:main",
    "bash_the_snake = snakes.bash_the_snake:main"
]


with open("requirements.txt", 'r') as f:
    requires = [req.strip() for req in f.readlines()]

setuptools.setup(
    name=config.get("release", "name"),
    version=config.get("release", "version"),
    description=config.get("release", "description"),
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    #   install_requires=requires,
    package_data={
      "snakes": ["nyan"]
      },
    entry_points={
      "snake_scripts": scripts,
      "console_scripts": scripts
      }
    )
