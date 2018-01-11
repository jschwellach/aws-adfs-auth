# aws-adfs-auth
aws-adfs-auth is a small utility to authenticate against a SAML provider with AWS.
It will authenticate against the federation provider and then get a temporary aws token.

# Installation
Currently only tested with python 3.x but.
To install the software just run
```bash
python setup.py install
```

# Configuration
To configure, just call
```bash
aws_adfs_auth --configure
```
The config file is located int ~/.aws/adfs_auth.ini
