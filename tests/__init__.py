import unittest
from . import test_configuration

def aws_adfs_auth_test_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test_configuration)
    return suite
