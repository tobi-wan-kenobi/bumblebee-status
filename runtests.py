#!/usr/bin/env python

import unittest

if __name__ == "__main__":
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTest(loader.discover("tests/"))

    unittest.TextTestRunner(verbosity=2).run(suite)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
