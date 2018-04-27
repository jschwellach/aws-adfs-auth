'''
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
'''

import os
import configparser
from os.path import expanduser


class Configure(object):
    home = expanduser("~")
    aws_folder = home + '/.aws'
    aws_adfs_auth_config_file = aws_folder + '/adfs_auth.ini'
    adfs_poviders = ['Microsoft']

    def __init__(self, logger):
        self.logger = logger

    def open_config(self):
        self.logger.debug('Opening config from file %s' % self.aws_adfs_auth_config_file)
        config = configparser.RawConfigParser()
        config.read(self.aws_adfs_auth_config_file)
        return config

    def check_config(self):
        """Function to check if the configuration is set."""
        self.logger.debug('checking config folders and files')
        if not os.path.exists(self.aws_folder):
            os.makedirs(self.aws_folder)
            self.logger.info("aws folder doesn't exist. App is not configured")
            return False
        if not os.path.isfile(self.aws_adfs_auth_config_file):
            self.logger.info("aws config file doesn't exist. App is not configured")
            return False
        config = self.open_config()
        if (not config.has_section('provider') or not
               config.has_option('provider', 'name') or not
               config.has_option('provider', 'idpentryurl')):
            self.logger.info("sanity check failed on config file. App is not configured")
            return False
        return True

    def store_config(self, config):
        """Function to store the configuration."""
        self.logger.debug("storing config file to %s" % self.aws_adfs_auth_config_file)
        with open(self.aws_adfs_auth_config_file, 'w+') as adfs_auth_config_file:
            config.write(adfs_auth_config_file)

    def setup_provider(self, config):
        """Function to setup the provider."""
        print("Please choose which ADFS provider you want to use (currently only Microsoft is supported)")
        if len(self.adfs_poviders) > 1:
            i = 0
            for adfs_provider in self.adfs_poviders:
                print('[{:2d}]: {:30s}'.format(i, adfs_provider))
                i += 1
            selected_provider_index = int(input('Selection: '))
        else:
            selected_provider_index = 0
        if not config.has_section('provider'):
            config.add_section('provider')
        config.set('provider', 'name', self.adfs_poviders[selected_provider_index])

    def setup_idpentryurl(self, config):
        """Function to setup the idp entry url."""
        self.logger.debug("setting up idp url")
        print("Please enter the ADFS provider enty URL for your configuration")
        print("Example: https://<provider>/adfs/ls/IdpInitiatedSignOn.aspx?loginToRp=urn:amazon:webservices")
        self.input_and_set(config=config, section='provider', option='idpentryurl', label='URL')

    def setup_profile_name(self, config):
        """Function to setup the profile name to use for storing the credentials."""
        self.logger.debug("setting up the profile name")
        print("Please enter the AWS profile you want to use for storing your credentials")
        print("If you use the default profile you don't need to specify the profile when executing AWS commands.")
        print("Make a backup of your default profile if you still need it.")
        self.input_and_set(config=config, section='provider', option='profile_name', label='AWS Profile')

    def input_and_set(self, config, section, option, label):
        """Function to ask for input and if the value is already set it will use the same value on pressing enter."""
        if not config.has_section(section):
            config.add_section(section)
        if config.has_option(section, option):
            last_value = config.get(section, option)
            value = input('{:s} [{:s}]: '.format(label, last_value)) or last_value
        else:
            value = input('{:s}: '.format(label))
        config.set(section, option, value)
        return value

    def set_value(self, config, section, option, value):
        """Function to set a value within the section."""
        if not config.has_section(section):
            config.add_section(section)
        if not config.has_option(section, option):
            config.set(section, option, value)

    def setup_variables(self, config):
        """Function to setup additional variables."""
        print("Please enter the AWS region")
        self.input_and_set(config=config, section='aws', option='region', label='Region')
        self.input_and_set(config=config, section='aws', option='outputformat', label='Output format')

    def setup_defaults(self, config):
        """Function to setup defaults."""
        self.set_value(config, 'aws', 'credentials_file', self.home + '/.aws/credentials')
        self.set_value(config, 'aws', 'sslverification', True)
        self.set_value(config, 'info', 'version', '0.4.0')
        self.set_value(config, 'provider', 'profile_name', 'saml')

    def setup(self):
        """Function to setup the configuration of adfs auth."""
        config = self.open_config()
        self.setup_provider(config)
        self.setup_idpentryurl(config)
        self.setup_variables(config)
        self.setup_defaults(config)
        self.setup_profile_name(config)
        self.store_config(config)
        return config

    def migrate_020_030(self, config):
        self.set_value(config, 'info', 'version', '0.3.0')
        self.set_value(config, 'provider', 'profile_name', 'saml')
        self.store_config(config)

    def migrate_030_040(self, config):
        self.set_value(config, 'info', 'version', '0.4.0')
        self.set_value(config, 'aws', 'set_environment_variables', False)
        self.set_value(config, 'aws', 'environment_file', self.home + '/.aws/environment.sh')
        self.store_config(config)

    def migrate(self, config):
        """Function to migrate the configuration to the next version."""
        self.logger.info('migrating configuration file to the latest version if necessary')
        # checking if config has a version number, if not we start to migrate from 0.2.0
        if not config.has_section('info'):
            config.add_section('info')
        if not config.has_option('info', 'version'):
            version = '0.2.0'
        else:
            version = config.get('info', 'version')
        if version == '0.4.0':
            # all good, we are on the latest version
            self.logger.info('migration of configuration not necessary.')
        elif version == '0.2.0':
            self.logger.info('migrating configuration from 0.2.0 to 0.3.0')
            self.migrate_020_030(config)
        elif version == '0.3.0':
            self.logger.info('migrating configuration from 0.3.0 to 0.4.0')
            self.migrate_030_040(config)
        else:
            raise Exception('configuration file corrupted, please re-configure application')
