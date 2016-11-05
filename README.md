docker-jinja - dj
=================

Extend your dockerfiles with Jinja2 syntax and logic.

Create new filter and functions for Jinja with simple datasource files.

Build status: [![Build Status](https://travis-ci.org/Grokzen/docker-jinja.svg?branch=master)](https://travis-ci.org/Grokzen/docker-jinja) [![Coverage Status](https://coveralls.io/repos/Grokzen/docker-jinja/badge.png)](https://coveralls.io/r/Grokzen/docker-jinja)



Installation
------------

Install from pypi with `pip install docker-jinja`

To install in development mode, first navigate to root of project and then run `pip install -r dev-requirements.txt; pip install -e .`. It is recommended to install inside a virtualenv to avoid conflicts with dependencies.



Quickstart guide
----------------

Create a Dockerfile.jinja that contains all regular Dockerfile build steps and the jinja syntax. For exapmle:

```
$ cat Dockerfile.jinja 
FROM {{ OS }}
MAINTAINER {{ MAINTAINER }} 

ARG {{ ARG1 }}
```

Run `dj` command. For example:

```
dj --dockerfile Dockerfile.jinja --outfile Dockerfile --env OS=ubuntu:12.04 --env MAINTAINER=Grokzen --env ARG1=foobar --config test-config.json
```

And you will get the output:

```
FROM ubuntu:12.04
MAINTAINER Grokzen

ARG foobar
```


Configuration files
-------------------

It is possible to create predefined configuration files with settings, enviroment variables and datasources.

`dj` tries to load the following configuration files in the following order:

- /etc/dj.yaml
- /etc/dj.json
- ~/.dj.yaml
- ~/.dj.json
- $CWD + '.dj.yaml'
- $CWD + '.dj.json'

YAML is the file format to prefer but json is also supported.

Currently it is not possible to automatically load a config file next to the source Dockerfile.



Datasources
-----------

If you want to extend the Jinja syntax with additional filters and global functions you have the datasource pattern to help you.

A datasource file is a python script that can contain any code you want so you can extend `dj` to be capable to perform any task you want.

You can tell `dj` to load a datasource file in multiple ways.

- In any config file create a key `datasources` with a list of strings paths pointing to all files that `dj` should import. (Must be absolute path)
- Point to a file with cli key -s/--datasource and `dj` will load that file. (Relative paths is supported)
- Add a python file to contrib folder and it will auto load during execution.



Global functions
################

A global function is a regular python function that you can call from jinja. These functions can be used to perform any usefull task you require.

To create a global function you define a method within a datasource and its name should starts with `_global_` and then follow by the name you want to use in your Dockerfile.

For example if you have the following code:

```python
def _global_foo():
    return "bar" 
```

You can call it from jinja with:

```Shell
RUN echo '{{ foo() }}'
```

and it will render into

```Shell
RUN echo 'bar'
```



Filter functions
################

To create a new filter function you define a method within a datasource and its name should starts with `_filter_` and then follow by the name you want to use in your Dockerfile.

For example if you have the following code

```python
def _filter_bar(arg):
    return arg.upper()
```

You can call it from jinja with:

```Shell
RUN echo '{{ "opa"|bar }}'
```

and it will render into

```Shell
RUN echo 'OPA'
```



Other rendering engines
-----------------------

Currently only Jinja2 is supported as rendering engine



Supported python version
------------------------

- 2.7
- 3.3
- 3.4

Python 3.2 will not be supported because Jinja2 is only supported on python >= 3.3 (Reference: http://jinja.pocoo.org/docs/intro/). If other rendering engines would be supported then python 3.2 can be supported for those engines.



Contribute
----------

Open an Issue on github describing the problem you have.

If you have a fix for the problem or want to add something to contrib library, open a PR with your fix. The PR must contain some test to verify that it work if it is a bugfix or new feature.  All tests in all supported python environments must pass on TravisCI before a PR will be accepted.

All PR:s should have their commits squashed to a single commit.



License
=======

See LICENSE file. (MIT)
