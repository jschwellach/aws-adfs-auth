from requests import Session
from robobrowser import RoboBrowser
import boto3
import xml.etree.ElementTree as ET
from os.path import expanduser
import configparser
import getpass
import base64
from . import configuration, utils


class AbstractADFS(object):
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self.configure = configuration.Configure(logger)
        if not self.config.has_section('aws_accounts'):
            self.config.add_section('aws_accounts')
        self.aws_accounts = config._sections['aws_accounts']

    def get_username_password(self):
        print ('Please enter your federation credentials')
        self.username = self.configure.input_and_set(self.config,'msadfs','username','Username')
        self.password = getpass.getpass()
        print ('')
        return self.username, self.password

    def delete_username_password(self):
        self.username = '##############################################'
        self.password = '##############################################'
        del self.username
        del self.password

    def init_browser(self):
        # Using RoboBrowser to get the SAML token
        self.browser = RoboBrowser(parser='lxml')
        self.browser.open(self.config.get('provider','idpentryurl'))
        return self.browser

    def handle_saml(self):
        self.logger.debug("handling saml response and finding out aws roles")
        browser = self.browser
        # Decode the response and extract the SAML assertion
        assertion = ''

        # Look for the SAMLResponse attribute of the input tag (determined by
        # analyzing the debug print lines above)
        for inputtag in browser.find_all('input'):
            if(inputtag.get('name') == 'SAMLResponse'):
                #print(inputtag.get('value'))
                assertion = inputtag.get('value')

        # Better error handling is required for production use.
        if (assertion == ''):
            #TODO: Insert valid error checking/handling
            print ('Response did not contain a valid SAML assertion')
            sys.exit(0)

        # Debug only
        #print(base64.b64decode(assertion))

        # Parse the returned assertion and extract the authorized roles
        awsroles = []
        root = ET.fromstring(base64.b64decode(assertion))
        for saml2attribute in root.iter('{urn:oasis:names:tc:SAML:2.0:assertion}Attribute'):
            if (saml2attribute.get('Name') == 'https://aws.amazon.com/SAML/Attributes/Role'):
                for saml2attributevalue in saml2attribute.iter('{urn:oasis:names:tc:SAML:2.0:assertion}AttributeValue'):
                    awsroles.append(saml2attributevalue.text)

        # Note the format of the attribute value should be role_arn,principal_arn
        # but lots of blogs list it as principal_arn,role_arn so let's reverse
        # them if needed
        for awsrole in awsroles:
            chunks = awsrole.split(',')
            if'saml-provider' in chunks[0]:
                newawsrole = chunks[1] + ',' + chunks[0]
                index = awsroles.index(awsrole)
                awsroles.insert(index, newawsrole)
                awsroles.remove(awsrole)

        # If I have more than one role, ask the user which one they want,
        # otherwise just proceed
        print ("")
        if len(awsroles) > 1:
            i = 0
            print ("Please choose the role you would like to assume:")
            for awsrole in awsroles:
                role = awsrole.split(',')[0]
                roleName = role.split(':')[5]
                accountId = role.split(':')[4]
                if accountId in self.aws_accounts:
                    print ('[{:2d}]: {:10s} {:30s}:{:10s}'.format(i,accountId, self.aws_accounts.get(accountId),roleName))
                else:
                    print ('[', i, ']: ', role)
                i += 1

            selectedroleindex = self.configure.input_and_set(config=self.config,section='msadfs',option='selectedroleindex',label='Selection')

            # Basic sanity check of input
            if int(selectedroleindex) > (len(awsroles) - 1):
                print ('You selected an invalid role index, please try again')
                sys.exit(0)

            role_arn = awsroles[int(selectedroleindex)].split(',')[0]
            principal_arn = awsroles[int(selectedroleindex)].split(',')[1]
        else:
            role_arn = awsroles[0].split(',')[0]
            principal_arn = awsroles[0].split(',')[1]

        self.configure.store_config(self.config)

        # Use the assertion to get an AWS STS token using Assume Role with SAML
        stsResponse = boto3.client('sts').assume_role_with_saml(
            RoleArn=role_arn,
            PrincipalArn=principal_arn,
            SAMLAssertion=assertion,
            DurationSeconds=3600 # is currently the maximum
        )

        # Write the AWS STS token into the AWS credential file
        filename = self.config.get('aws','credentials_file')

        # Read in the existing config file
        awsconfig = configparser.RawConfigParser()
        awsconfig.read(filename)

        # Put the credentials into a saml specific section instead of clobbering
        # the default credentials
        if not awsconfig.has_section('saml'):
            awsconfig.add_section('saml')

        awsconfig.set('saml', 'output', self.config.get('aws','outputformat'))
        awsconfig.set('saml', 'region', self.config.get('aws','region'))
        awsconfig.set('saml', 'aws_access_key_id', stsResponse['Credentials']['AccessKeyId'])
        awsconfig.set('saml', 'aws_secret_access_key', stsResponse['Credentials']['SecretAccessKey'])
        awsconfig.set('saml', 'aws_session_token', stsResponse['Credentials']['SessionToken'])

        # Write the updated config file
        with open(filename, 'w+') as configfile:
            awsconfig.write(configfile)

        # Give the user some basic info as to what has just happened
        print ('\n\n----------------------------------------------------------------')
        print ('Your new access key pair has been stored in the AWS configuration file {0} under the saml profile.'.format(filename))
        print ('Note that it will expire at {0}.'.format(stsResponse['Credentials']['Expiration']))
        print ('After this time, you may safely rerun this script to refresh your access key pair.')
        print ('To use this credential, call the AWS CLI with the --profile option (e.g. aws --profile saml ec2 describe-instances).')
        print ('----------------------------------------------------------------\n\n')
