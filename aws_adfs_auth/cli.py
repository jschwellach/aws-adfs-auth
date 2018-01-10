"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

import sys
import argparse

def init():
    """ process command line arguments """
    parser = argparse.ArgumentParser(description="Request temporary AWS account credentials "
                                                 "for a federated account",
                                     usage="%(prog)s [options]",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="""
NOTE: If you have several aws accounts where you have access to, you can map them in the config file (~/.aws/adfs_auth.ini) to a suitable name.
EXAMPLE:
...
[aws_accounts]
123456789 = Production
234567890 = Staging
345678901 = Development
...

""")

    parser.add_argument("-V", "--version",
                        dest="show_version", action="store_true",
                        help="Show the version number and exit")

    parser.add_argument("-C", "--configure",
                        dest="configure", action="store_true",
                        help="Configures the AWS ADFS Auth application")

    parser.add_argument("-v", "--verbose",
                        dest="verbosity", action="count",
                        help="Output debug messages, increase messages with -v -v")
    return parser

def show_version():
    """ show version and exit """
    print("aws_adfs_auth version:{}".format(sys.modules["aws_adfs_auth"].VERSION))
    sys.exit(0)

def error(message):
    """ display an error related to command line arguments and quit """
    print(message + "\nhint: try -h for help")
    sys.exit(1)

def check_args():
    """ checking the command line arguments """
    parser = init()
    parsed_options = parser.parse_args()

    if parsed_options.show_version:
        show_version()


    return parsed_options
