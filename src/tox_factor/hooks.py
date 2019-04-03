import os

import tox

from .factor import get_envlist


def envlist(name):
    # VAR=foo,bar => ['foo', 'bar']
    factors = os.environ.get(name, '')
    factors = [f.strip() for f in factors.split(',') if f]

    return factors


@tox.hookimpl
def tox_addoption(parser):
    parser.add_argument(
        '-f', '--factor', action='append', default=envlist('TOXFACTOR'),
        help='work against environments that match the given factors.')


@tox.hookimpl
def tox_configure(config):
    ini = config._cfg

    # Do not match factors when tox env is specified
    if 'TOXENV' in os.environ or config.option.env:
        return

    if config.option.factor:
        config.envlist = get_envlist(ini, config.option.factor)
