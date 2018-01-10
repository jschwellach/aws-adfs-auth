import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from aws_adfs_auth import configure
from aws_adfs_auth.ms_adfs import MicrosoftADFS

def test_msadfs():
    print("running msafgs test")
    config = configure.setup()
    result = configure.check_config()
    assert result == True
    adfs = MicrosoftADFS(config)
