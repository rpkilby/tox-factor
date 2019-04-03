import mock
from unittest import TestCase

from tox_factor.hooks import tox_configure


class ToxConfigureHookTests(TestCase):
    # Note that we don't test `TOXFACTOR` and `-f <factor>` separately, as the
    # argparse defaults value *is the `TOXFACTOR` env variable. Effectively,
    # `config.options.factor` represents both cases.

    @mock.patch('tox_factor.hooks.get_envlist')
    def test_default_noop(self, get_envlist):
        # mimics: `tox`
        config = mock.Mock()
        config.option.env = []
        config.option.factor = []

        tox_configure(config)

        get_envlist.assert_not_called()

    @mock.patch('tox_factor.hooks.get_envlist')
    def test_toxfactor(self, get_envlist):
        # mimics: `tox -f test` and `TOXFACTOR=test tox`
        config = mock.Mock()
        config.option.env = []
        config.option.factor = ['test']

        tox_configure(config)

        get_envlist.assert_called_once_with(config._cfg, ['test'])

    @mock.patch('tox_factor.hooks.get_envlist')
    def test_toxenv_option_supersedes_toxfactor(self, get_envlist):
        # mimics: `tox -e test -f test`
        config = mock.Mock()
        config.option.env = 'test'
        config.option.factor = 'test'

        tox_configure(config)

        get_envlist.assert_not_called()

    @mock.patch('tox_factor.hooks.get_envlist')
    @mock.patch.dict('os.environ', {'TOXENV': 'test'})
    def test_toxenv_envvar_supersedes_toxfactor(self, get_envlist):
        # mimics: `TOXENV=test tox -f test`
        config = mock.Mock()
        config.option.factor = 'test'

        tox_configure(config)

        get_envlist.assert_not_called()

    @mock.patch('tox_factor.hooks.get_envlist')
    @mock.patch.dict('os.environ', {'TOXENV': 'test'})
    def test_toxenv_envvar_and_option_supersedes_toxfactor(self, get_envlist):
        # mimics: `TOXENV=test tox -e test -f test`
        config = mock.Mock()
        config.option.env = 'test'
        config.option.factor = 'test'

        tox_configure(config)

        get_envlist.assert_not_called()
