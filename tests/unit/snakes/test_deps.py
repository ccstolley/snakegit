from mock import Mock, patch
import unittest

from snakes.deps import requirements


class TestDeps(unittest.TestCase):

    def test_private_requirements(self):
        mock_open = Mock()
        fp_mock = Mock()
        req_string = """
foo==1.2.4b
bar>=1.3


"""
        mock_open.return_value = fp_mock
        fp_mock.__enter__ = Mock()
        fp_mock.__exit__ = Mock()
        fp_mock.__enter__.return_value.read.return_value = req_string
        expected_reqs = [
            {'name': 'foo', 'operator': '==', 'version': '1.2.4b'},
            {'name': 'bar', 'operator': '>=', 'version': '1.3'},
        ]
        with patch('__builtin__.open', mock_open):
            reqs = [r for r in requirements(req_string)]
        self.assertEqual(reqs, expected_reqs)
