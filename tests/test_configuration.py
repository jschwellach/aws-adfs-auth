import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from aws_adfs_auth import configure

def test_configure():
    print("running configuration test")
    configure.setup()
    result = configure.check_config()
    assert result == True
