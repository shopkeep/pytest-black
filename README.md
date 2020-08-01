pytest-black
============

[![Build Status](https://travis-ci.org/shopkeep/pytest-black.svg?branch=master)](https://travis-ci.org/shopkeep/pytest-black)

A pytest plugin to enable format checking with [black](https://github.com/ambv/black).


Requirements
------------

* [pytest](https://docs.pytest.org/en/latest/)
* [black](https://github.com/ambv/black)

There is a minimum requirement of black 19.3b0 or later.

Installation
------------

```
$ pip install pytest-black
```


Usage
-----

To run pytest with formatting checks provided by black:

```
$ pytest --black
```

The plugin will output a diff of suggested formatting changes (if any exist). Changes will _not_ be applied automatically.


Configuration
-------------

You can override default black configuration options by placing a `pyproject.toml` file in your project directory. See example configuration [here](https://github.com/ambv/black/blob/master/pyproject.toml).


Python package management
-------------------------
For *poetry* to work correctly, include this in your pyproject.toml configuration file:

```
[tool.poetry.dev-dependencies]
...
black = { version = "*", allow-prereleases = true }
...
```

This is necessary because at the time of writing all the *black* releases in PyPI have been tagged as pre-releases (beta code), which breaks *poetry*'s dependency resolution.


Testing
-------

To run the tests against a selection of Python interpreters:

```
$ tox
```

To run against a specific interpreter (e.g. Python 3.6):

```
$ tox -e py36
```

The `tox.ini` file in the root of this repository is used to configure the test environment.


License
-------

Distributed under the terms of the `MIT` license, `pytest-black` is free and open source software


Issues
------

If you encounter any problems, please [file an issue](https://github.com/shopkeep/pytest-black/issues) along with a detailed description.
