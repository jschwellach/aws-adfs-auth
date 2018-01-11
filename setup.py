from setuptools import setup
import sys
import os
import aws_adfs_auth

install_requires = [
    'markdown',
    'requests',
    'robobrowser',
    'boto3',
    'lxml',
    'pytest-runner'
]

tests_requires = [
    'pytest'
]


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = aws_adfs_auth.__title__,
    version = aws_adfs_auth.__version__,
    description = aws_adfs_auth.__summary__,
    long_description=read('README.md'),
    license = aws_adfs_auth.__license__,
    url = aws_adfs_auth.__uri__,
    author = aws_adfs_auth.__author__,
    author_email = aws_adfs_auth.__email__,
    packages=['aws_adfs_auth'],
    install_requires=install_requires,
    tests_require=tests_requires,
    extras_requires={},
    data_files= [("", ["LICENSE"])],
    entry_points={'console_scripts': ['aws_adfs_auth = aws_adfs_auth.main:main']},
    keywords = "",
    test_suite = 'tests.aws_adfs_auth_test_suite',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)
