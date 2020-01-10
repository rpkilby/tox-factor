import unittest

from tox_factor.test import ToxTestCase
from sys import version_info


class ToxTestCaseTests(unittest.TestCase):

    def test_error_message(self):
        class Dummy(ToxTestCase):
            pass

        with self.assertRaises(AssertionError) as excinfo:
            Dummy.setUpClass()

        self.assertEqual(
            str(excinfo.exception),
            '`tests.test_test.Dummy.ini_contents` has not been set.',
        )

    def test_tox_envlist(self):
        class Dummy(ToxTestCase):
            ini_contents = """
            [tox]
            envlist = py27,py37

            [testenv:lint]
            """

            def runTest(self):
                # fixes a Python 2 compatibility issue when instantiating a
                # test case outside of a test suite
                pass

        testcase = Dummy()

        try:
            testcase.setUpClass()
            envlist = testcase.tox_envlist()
        finally:
            testcase.tearDownClass()

        # by default, tox does not list testenvs not present in `envlist`.
        self.assertEqual(envlist, ['py27', 'py37'])

    def test_tox_call(self):
        class Dummy(ToxTestCase):
            ini_contents = """
            [testenv:lint]
            commands = python -c "print('clean')"
            """

            setup_contents = """
            from setuptools import setup

            setup(name='test')
            """

            def runTest(self):
                # fixes a Python 2 compatibility issue when instantiating a
                # test case outside of a test suite
                pass

        testcase = Dummy()

        try:
            testcase.setUpClass()
            returncode, stdout, stderr = testcase.tox_call(['-e', 'lint'])
        finally:
            testcase.tearDownClass()

        self.assertEqual(returncode, 0)
        self.assertIn('lint: commands succeeded', stdout)

    def test_tox_call_no_setup_module(self):
        class Dummy(ToxTestCase):
            ini_contents = """
            [testenv:lint]
            commands = python -c "print('clean')"
            """

            def runTest(self):
                # fixes a Python 2 compatibility issue when instantiating a
                # test case outside of a test suite
                pass

        testcase = Dummy()

        try:
            testcase.setUpClass()
            returncode, stdout, stderr = testcase.tox_call(['-e', 'lint'])
        finally:
            testcase.tearDownClass()

        self.assertNotEqual(returncode, 0)
        if version_info[0] == 3 and version_info[1] >= 5 or \
           version_info[0] == 2 and version_info[1] == 7:
            self.assertIn('ERROR: No pyproject.toml or setup.py file found.',
                          stdout)
        else:
            self.assertIn('ERROR: No setup.py file found.', stdout)
