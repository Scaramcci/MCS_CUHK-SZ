"""Run current offline behavioral tests; historical scaffold test is in history/."""

from pathlib import Path
import unittest

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover(str(Path(__file__).parent), pattern='test_core.py')
    outcome = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if outcome.wasSuccessful() else 1)
