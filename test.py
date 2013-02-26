import os.path, sys, glob
import unittest


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()

    for path in glob.glob("*/*.pyc"):
        path = path.replace("/",".")[:-4]

        __import__(path)
        mod = sys.modules[path]

        suite.addTests(loader.loadTestsFromModule(mod))

    return suite

if __name__ == "__main__":
    unittest.main()