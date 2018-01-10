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

import logging

def setup_logging(options):
    """ set up logging... """
    logger = logging.getLogger("aws_adfs_auth")
    logger.setLevel(logging.ERROR)
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s(%(threadName)s): %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    if options.verbosity is None:
        options.verbosity = 0
    if options.verbosity >= 1:
        logger.setLevel(logging.INFO)
    if options.verbosity >= 2:
        logger.setLevel(logging.DEBUG)
    logger.debug("Logger set up")
    return logger
