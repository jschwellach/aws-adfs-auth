# aws-adfs-auth
aws-adfs-auth is a small utility to authenticate against a SAML provider with AWS.
It will authenticate against the federation provider and then get a temporary aws token.

# Installation
To install the software just run
```bash
sudo pip3 install aws_adfs_auth
```

# Configuration
To configure, just call
```bash
aws_adfs_auth --configure
```
The config file is located int ~/.aws/adfs_auth.ini
Please refer to the help section if you have multiple accounts on AWS

# Contributing
This tool is open source, so feel free to contribute on github:
https://github.com/jschwellach/aws-adfs-auth

Please submit pull requests and I'll update the code to PyPi repository.

# Compiling
For compiling clone the repository https://github.com/jschwellach/aws-adfs-auth or fork it and then execute the following in a python 3 environment
```bash
python setup.py install
```
