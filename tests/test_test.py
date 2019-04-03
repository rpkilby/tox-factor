import unittest

from tox_factor.test import ToxTestCase


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
                pass  # Prevents an error in Python 2

        testcase = Dummy()
        testcase.setUpClass()

        try:
            envlist = testcase.tox_envlist()
        finally:
            testcase.tearDownClass()

        # by default, tox does not list testenvs not present in `envlist`.
        self.assertEqual(envlist, ['py27', 'py37'])
