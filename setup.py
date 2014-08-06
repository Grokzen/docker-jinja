#!/usr/bin/env python
import os
from setuptools import setup, find_packages

settings = dict()

# TODO: Load dependencies from requirements.txt file

long_description = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

settings.update(
    name='docker-jinja',
    version='0.1.0',
    description='Extend your dockerfiles with Jinja2 syntax to to more awesome dockerfiles',
    long_description=long_description,
    author='Johan Andersson',
    author_email='Grokzen@gmail.com',
    packages=find_packages(exclude=['.tox', '*test/']),
    scripts=['scripts/dj'],
    install_requires=[
        'PyYAML==3.11',
        'Jinja2==2.7.3',
        'docopt==0.6.2',
    ],
    license="MIT",
    url='https.//github.com/Grokzen/docker-jinja',
    classifiers=(
        #  As from https://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Environment :: Console',
        'Environment :: Docker',
        'Operating System :: POSIX',
        'Topic :: Docker',
        'Topic :: Dockerfile',
    )
)

setup(**settings)
