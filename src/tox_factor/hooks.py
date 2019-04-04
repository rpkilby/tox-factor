import os

import tox

from .factor import get_envlist


def normalize_factors(factors):
    """Normalize the factor list into a list of individual factors.

    The factor argument has "append" behavior (-f foo -f bar), and each of these
    arguments may be a comma-separated list of factors. Normalize this into a
    flat list of individual factors. e.g.,

        >>> normalize_factors(['py37', 'lint,isort'])
        ['py37', 'lint', 'isort']

    Args:
        factors: A list of comma-separated factor strings.

    Returns:
        The list flattened, individual factors.
    """
    assert isinstance(factors, list), (
        'Expected `factors` list to be a list, got `{cls}`.'
        .format(cls=type(factors).__name__))

    flattened = [
    ]

    # Remove empty strings
    return [f for f in flattened if f]


@tox.hookimpl
def tox_addoption(parser):
    parser.add_argument(  # pragma: no cover
        '-f', '--factor', action='append',
        help='work against environments that match the given factors.')


@tox.hookimpl
def tox_configure(config):
    ini = config._cfg

    # Do not match factors when tox env is specified
    if 'TOXENV' in os.environ or config.option.env:
        return

    # Append behavior does not override default. Set default here instead.
    # See: https://bugs.python.org/issue16399
    envvar = os.environ.get('TOXFACTOR')
    if not config.option.factor and envvar:
        config.option.factor = [envvar]

    if config.option.factor:
        factors = normalize_factors(config.option.factor)
        config.envlist = get_envlist(ini, factors)
