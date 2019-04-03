from tox.config import _split_env as split_env


def get_envlist(ini, factors):
    """Get the list of env names from the tox config that match the factors.

    See `match_envs` for more details on env name matching.

    Args:
        ini: The parsed tox ini config. This should be the `_cfg` attribute of
            the `config` passed to the `tox_configure` hook.
        factors: The list of env factors to match against.

    Returns:
        The list of env names from the tox config that match the given factors.
    """
    declared_envs = get_declared_envs(ini)

    return match_envs(declared_envs, factors)


def get_declared_envs(ini):
    """Get the full list of envs from the tox ini.

    This notably also includes envs that aren't in the envlist,
    but are declared by having their own testenv:envname section.

    The envs are expected in a particular order. First the ones
    declared in the envlist, then the other testenvs in order.

    Args:
        ini: The parsed tox ini config object.

    Returns:
        The list of env names defined in the tox config.
    """
    tox_section_name = 'tox:tox' if ini.path.endswith('setup.cfg') else 'tox'
    tox_section = ini.sections.get(tox_section_name, {})
    envlist = split_env(tox_section.get('envlist', []))

    # Add additional envs that are declared as sections in the ini
    section_envs = [
        section[8:] for section in sorted(ini.sections, key=ini.lineof)
        if section.startswith('testenv:')
    ]

    return envlist + [env for env in section_envs if env not in envlist]


def match_envs(env_names, factors):
    """Determine the subset of env names that match any of the given factors.

    See `env_matches` for more detail on env name matching behavior.

        >>> envlist = [
        >>>     'py36-django20', 'py36-django21',
        >>>     'py37-django20', 'py37-django21',
        >>> ]
        >>> match_envs(envlist, ['py37', 'django21'])
        ['py36-django21', 'py37-django20', 'py37-django21']

    Args:
        env_names: The list of env names to check.
        factors: The list of env factors to match against.

    Returns:
        The list of matched env names.
    """
    return [
        name for name in env_names
        if any(env_matches(name, factor) for factor in factors)
    ]


def env_matches(env_name, factor):
    """Determine if an env name matches the given factor.

    The env name is split into its component factors, and matches if the given
    factor is present in the component factors. Partial matches are not valid.

        >>> env_matches('py37-django21', 'py37')
        True

        >>> env_matches('py37-django21', 'py3')
        False

    The given factor may also consist of multiple dash-delimited factors, of
    which all must be present in the env name.

        >>> env_matches('py37-django21-redis', 'py37-redis')
        True

    Args:
        env_name: The tox test env name.
        factor: The env factor to match against.

    Returns:
        Whether the name matches the given factor(s).
    """
    env_factors = env_name.split('-')
    factors = factor.split('-')

    return set(factors).issubset(set(env_factors))
