import unittest

from snakes.deps import _requirements


class TestDeps(unittest.TestCase):

    def test_private_requirements(self):
        req_string = """
foo==1.2.4b
bar>=1.3


"""
        expected_reqs = [
            {'name': 'foo', 'operator': '==', 'version': '1.2.4b'},
            {'name': 'bar', 'operator': '>=', 'version': '1.3'}
        ]
        reqs = [r for r in _requirements(req_string)]
        self.assertEqual(reqs, expected_reqs)
