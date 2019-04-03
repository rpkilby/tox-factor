import unittest

from tox_factor import factor
from tox_factor.test import ToxTestCase


# get_envlist ##################################################################
class GetEnvlistTests(ToxTestCase):
    ini_contents = """
    [tox]
    envlist = py{36,37}-django{20,21}

    [testenv:lint]
    [testenv:isort]
    """

    def test_single_factor(self):
        self.assertEqual(
            factor.get_envlist(self.config, ['py37']),
            ['py37-django20', 'py37-django21'],
        )

    def test_multiple_factors(self):
        self.assertEqual(
            factor.get_envlist(self.config, ['py37', 'django21']),
            ['py36-django21', 'py37-django20', 'py37-django21'],
        )

    def test_combined_factors(self):
        self.assertEqual(
            factor.get_envlist(self.config, ['py37', 'lint']),
            ['py37-django20', 'py37-django21', 'lint'],
        )


# get_declared_envs ############################################################
class GetDeclaredEnvsEnvlistTests(ToxTestCase):
    ini_contents = """
    [tox]
    envlist = py27,py37
    """

    def test_result(self):
        self.assertEqual(
            factor.get_declared_envs(self.config),
            ['py27', 'py37'],
        )


class GetDeclaredEnvsGenerativeEnvlistTests(ToxTestCase):
    ini_contents = """
    [tox]
    envlist = py{27,37}
    """

    def test_result(self):
        self.assertEqual(
            factor.get_declared_envs(self.config),
            ['py27', 'py37'],
        )


class GetDeclaredEnvsTestenvsTests(ToxTestCase):
    ini_contents = """
    [testenv:lint]
    [testenv:isort]
    """

    def test_result(self):
        self.assertEqual(
            factor.get_declared_envs(self.config),
            ['lint', 'isort'],
        )


class GetDeclaredEnvsCombinedTests(ToxTestCase):
    ini_contents = """
    [tox]
    envlist = py{27,37}

    [testenv:lint]
    [testenv:isort]
    """

    def test_result(self):
        self.assertEqual(
            factor.get_declared_envs(self.config),
            ['py27', 'py37', 'lint', 'isort'],
        )


# match_envs ###################################################################
class MatchEnvsTests(unittest.TestCase):
    testenvs = [
        'py36-django20',
        'py36-django21',
        'py37-django20',
        'py37-django21',
    ]

    def test_no_factors(self):
        self.assertEqual(
            factor.match_envs(self.testenvs, []),
            [],
        )

    def test_non_existent_factor(self):
        self.assertEqual(
            factor.match_envs(self.testenvs, ['foo']),
            [],
        )

    def test_single_factor(self):
        self.assertEqual(
            factor.match_envs(self.testenvs, ['py37']),
            ['py37-django20', 'py37-django21'],
        )

    def test_multiple_factors(self):
        self.assertEqual(
            factor.match_envs(self.testenvs, ['py37', 'django20']),
            ['py36-django20', 'py37-django20', 'py37-django21'],
        )


# env_matches ##################################################################
class EnvMatchesTests(unittest.TestCase):
    def test_exact(self):
        self.assertTrue(factor.env_matches('py37', 'py37'))

    def test_multiple_exact(self):
        self.assertTrue(factor.env_matches('py37-django21', 'py37-django21'))

    def test_multiple_exact_unordered(self):
        self.assertTrue(factor.env_matches('py37-django21', 'django21-py37'))

    def test_disjoint_factor_match(self):
        self.assertTrue(factor.env_matches('py37-django21-redis', 'py37-redis'))

    def test_non_existent_factor(self):
        self.assertFalse(factor.env_matches('py37', 'foo'))
        self.assertFalse(factor.env_matches('py37-django21', 'foo'))
        self.assertFalse(factor.env_matches('py37-django21', 'foo-bar'))

    def test_partial_factor_set_match(self):
        self.assertFalse(factor.env_matches('py37-django21', 'py37-bar'))

    def test_partial_factor_term_match(self):
        self.assertFalse(factor.env_matches('py37', 'py3'))
