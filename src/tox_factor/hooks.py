import os

import tox
from tox.config.parallel import ENV_VAR_KEY as TOX_PARALLEL_ENV

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
        f.strip()
        for flist in factors
        for f in flist.split(',')
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
    # Run on the main tox process but not in the parallelized subprocesses,
    # where the subprocess has been delegated a specific TOX_PARALLEL_ENV.
    if TOX_PARALLEL_ENV in os.environ:
        return

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
        config.envlist = get_envlist(config._cfg, factors)

        # TEMP: setting config.envlist_default fixes tox -l usage (and by
        # extension, the test suite). The longterm fix is to add a new option
        # to tox (e.g., tox -ls) that lists the selected envs (config.envlist).
        config.envlist_default = config.envlist
