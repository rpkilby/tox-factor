import mock

from tox_factor.test import ToxTestCase


class ToxFactorIntegrationTests(ToxTestCase):
    ini_contents = """
    [tox]
    envlist = py{36,37}-django{20,21}

    [testenv:lint]
    [testenv:isort]
    """

    def test_baseline(self):
        self.assertEqual(
            self.tox_envlist(),
            [
                'py36-django20', 'py36-django21',
                'py37-django20', 'py37-django21'
            ],
        )

    def test_abbreviated(self):
        self.assertEqual(
            self.tox_envlist(['-f', 'py37']),
            [
                'py37-django20', 'py37-django21'
            ],
        )

    def test_argument(self):
        self.assertEqual(
            self.tox_envlist(['--factor', 'py37']),
            [
                'py37-django20', 'py37-django21'
            ],
        )

    @mock.patch.dict('os.environ', {'TOXFACTOR': 'py37'})
    def test_environment_variable(self):
        self.assertEqual(
            self.tox_envlist(),
            [
                'py37-django20', 'py37-django21'
            ],
        )
