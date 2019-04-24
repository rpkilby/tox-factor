import mock
from unittest import TestCase

from tox.config.parallel import ENV_VAR_KEY as TOX_PARALLEL_ENV

from tox_factor.hooks import normalize_factors, tox_configure


class NormalizeFactorsTests(TestCase):
    def test_sanity_check(self):
        with self.assertRaises(AssertionError) as excinfo:
            normalize_factors(None)

        self.assertEqual(
            str(excinfo.exception),
            "Expected `factors` list to be a list, got `NoneType`.",
        )

    def test_empty(self):
        self.assertEqual(
            normalize_factors([]),
            [],
        )
        self.assertEqual(
            normalize_factors(['']),
            [],
        )

    def test_single_factor(self):
        self.assertEqual(
            normalize_factors(['py37']),
            ['py37'],
        )

    def test_list_of_factors(self):
        self.assertEqual(
            normalize_factors(['py27', 'py37']),
            ['py27', 'py37'],
        )

    def test_list_of_factor_lists(self):
        self.assertEqual(
            normalize_factors(['py37', 'isort,lint']),
            ['py37', 'isort', 'lint'],
        )

    def test_whitespace_stripping(self):
        self.assertEqual(
            normalize_factors([' ', 'isort , lint ']),
            ['isort', 'lint'],
        )


class ToxConfigureHookTests(TestCase):

    @mock.patch('tox_factor.hooks.get_envlist')
    def test_default_noop(self, get_envlist):
        # mimics: `tox`
        config = mock.Mock()
        config.option.env = []
        config.option.factor = []

        tox_configure(config)

        get_envlist.assert_not_called()

    @mock.patch('tox_factor.hooks.get_envlist')
    def test_toxfactor_option(self, get_envlist):
        # mimics: `tox -f test`
        config = mock.Mock()
        config.option.env = []
        config.option.factor = ['test']

        tox_configure(config)

        get_envlist.assert_called_once_with(config._cfg, ['test'])

    @mock.patch('tox_factor.hooks.get_envlist')
    @mock.patch.dict('os.environ', {'TOXFACTOR': 'test'})
    def test_toxfactor_envvar(self, get_envlist):
        # mimics: `TOXFACTOR=test tox`
        config = mock.Mock()
        config.option.env = []
        config.option.factor = []

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

    @mock.patch('tox_factor.hooks.get_envlist')
    @mock.patch.dict('os.environ', {TOX_PARALLEL_ENV: 'test'})
    def test_tox_parallel_env_envvar_noop(self, get_envlist):
        # mimics: `TOX_PARALLEL_ENV=test tox`
        config = mock.Mock()

        tox_configure(config)

        get_envlist.assert_not_called()
