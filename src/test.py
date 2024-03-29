# -*- coding: utf-8 -*-
"""Run all the tests"""
import unittest


if __name__ == '__main__':
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)