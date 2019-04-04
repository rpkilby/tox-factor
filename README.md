# tox-factor

[![CircleCI](https://circleci.com/gh/rpkilby/tox-factor.svg?style=shield)](https://circleci.com/gh/rpkilby/tox-factor)
[![Appveyor](https://ci.appveyor.com/api/projects/status/8yqgrr22dct9rxxg?svg=true)](https://ci.appveyor.com/project/rpkilby/tox-factor)
[![codecov](https://codecov.io/gh/rpkilby/tox-factor/branch/master/graph/badge.svg)](https://codecov.io/gh/rpkilby/tox-factor)
[![version](https://img.shields.io/pypi/v/tox-factor.svg)](https://pypi.python.org/pypi/tox-factor)
[![python](https://img.shields.io/pypi/pyversions/tox-factor.svg)](https://pypi.org/project/tox-factor/)
[![license](https://img.shields.io/pypi/l/tox-factor.svg)](https://pypi.python.org/pypi/tox-factor)

## What is tox-factor?

tox-factor enables running a subset of tox test envs, based on factor matching.


## Okay, but what does that *actually* mean?

Take the following tox config:

```ini
[tox]
envlist =
    py{35,36,37}-django{20,21,22}-{redis,memcached}
```

The above defines 18 test envs, based on three factor groups - the python
version, the django version, and a caching backend. While the above is powerful,
tox does not provide a way to run builds based on a subset of those factors.
For example, the call to run all Python 3.7 builds would be:

```shell
$ tox -e py37-django20-redis,py37-django20-memcached,py37-django21-redis,py37-django21-memcached,py37-django22-redis,py37-django22-memcached
```

tox-factor functions similarly to the `-e <env name>` argument, except it runs
all envs that match the given factor. The six `py37` builds could be ran with:

```shell
$ tox -f py37
```

In addition to ease of use when running tox locally, this is useful for some CI
setups. For example, two common tox CI patterns are to either:

- Define a CI job for each tox test env. e.g.,

    `tox -e py37-django20-redis`

- Define a CI job for a common environment that runs multiple test envs. e.g.,

    `tox -e py37-django20-redis,py37-django20-memcached,...`

For the latter case, this plugin eases maintenance of CI, as it could be
shortened to `tox -f py37`. Additionally, take the following update to the above
tox config:

```ini
[tox]
envlist =
    py{35,36,37}-django{20,21,22}-{redis,memcached}
    py{36,37,38}-django{30}-{redis,memcached}
```

By using tox-factor, it wouldn't be necessary to update the Python 3.7 build, as
the new `py37-django30-*` env would be matched automatically.



## Verifying the matched test envs

If you want to verify which test envs are actually ran, combine the factor
matching with the `-l` flag. This will display all test envs that match. e.g.,

```shell
$ tox -f py37 -l
py37-django20-redis
py37-django20-memcached
py37-django21-redis
py37-django21-memcached
py37-django22-redis
py37-django22-memcached
```


## Usage details

The factor option accepts a comma-separated list (similar to the `-e` option).
```shell
$ tox -f py27,py37 -l
py27-django111
py37-django21
```

Alternatively, factors can be provided via the `TOXFACTOR` environment variable:
```shell
$ TOXFACTOR=py27,py37 tox -l
py27-django111
py37-django21
```

Factors can also match non-generative env names. For example, given the
following tox config:

```ini
[tox]
envlist =
    py{35,36,37}-django20

[testenv:list]
```

Then the following would match:

```shell
$ tox -f py37,lint -l
py37-django20
lint
```

Factors are always superseded by a given `toxenv`. For example, tox-factor would
noop in the following cases:

```shell
$ tox -f py37 -e py35-django21 -l
py35-django21

$ TOXENV=py35-django21 tox -f py37 -l
py35-django21
```

Factors do not support partial matching. `tox -f py3` would not match `py37`.
However, factors may match disparate dash-separated parts. Given the following:
```ini
[tox]
envlist =
    py{35,36,37}-django{20,21,22}-{redis,memcached}
```

Then `tox -f py37-redis` would match:
```
py37-django20-redis
py37-django21-redis
py37-django22-redis
```


## Release Process

- Update changelog
- Update package version in setup.py
- Create git tag for version
- Upload release to PyPI test server
- Upload release to official PyPI server

```shell
$ pip install -U pip setuptools wheel twine
$ rm -rf dist/ build/
$ python setup.py sdist bdist_wheel
$ twine upload -r test dist/*
$ twine upload dist/*
```


## Thanks

This code is largely based off the work done by @ryanhiebert in [tox-travis][1].
Without his efforts, it would have taken significantly more time to write and
test this package.

## License

See: [LICENSE][2]

[1]: https://github.com/tox-dev/tox-travis
[2]: https://github.com/rpkilby/tox-factor/blob/master/LICENSE
