from . import abstract_adfs

class MicrosoftADFS:

    def __init__(self, logger, config):
        logger.info("initialize MicrosoftADFS")
        self.logger = logger
        self.config = config
        self.adfs = abstract_adfs.AbstractADFS(logger,config)

        username, password = self.adfs.get_username_password()

        browser = self.adfs.init_browser()
        if (browser.find(id='loginForm')):
            form = browser.get_form(id='loginForm')
            form["UserName"] = username
            form["Password"] = password
        else:
            print ('Could not find the required forms. Maybe different provider')
            sys.exit(1)

        # Submitting the form
        browser.submit_form(form)

        self.adfs.delete_username_password()
        self.adfs.handle_saml()
