pytest-black
============

[![Build Status](https://travis-ci.org/shopkeep/pytest-black.svg?branch=master)](https://travis-ci.org/shopkeep/pytest-black)

A pytest plugin to enable format checking with [black](https://github.com/ambv/black).


Requirements
------------

* [pytest](https://docs.pytest.org/en/latest/)
* [black](https://github.com/ambv/black)


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
