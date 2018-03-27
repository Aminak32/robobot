import mechanicalsoup
import time

import re
from mechanicalsoup import LinkNotFoundError

from appProxyHandler import AppProxyHandler


class ClFormSubmitter:
    proxies = {}

    clLoginUrl = "https://accounts.craigslist.org/login"


    def clLoginSubmit(self, clUsername, clPassword):
        self.setProxy()

        browser = mechanicalsoup.StatefulBrowser(
            soup_config={'features': 'lxml'},
            raise_on_404=True,
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        )
        # browser.set_verbose(2)

        browser.session.proxies = self.proxies
        try:
            browser.open(self.clLoginUrl)
            browser.select_form('.loginform')
        except LinkNotFoundError:
            return False

        browser["inputEmailHandle"] = clUsername
        browser["inputPassword"] = clPassword

        clLoginPageTitle = browser.get_current_page().find('title')
        resp = browser.submit_selected()
        clAfterLoginSubmitUrl = browser.get_url()
        clAfterLoginPageTitle = browser.get_current_page().find('title')

        if resp.status_code == 200:
            if (clLoginPageTitle == clAfterLoginPageTitle) or (self.clLoginUrl.split('?')[0] == clAfterLoginSubmitUrl.split('?')[0]):
                return False
            else:
                return True



    def clPostPickerFormSubmit(self, url, val, guiElem):
        self.setProxy()

        browser = mechanicalsoup.StatefulBrowser(
            soup_config={'features': 'lxml'},
            raise_on_404=True,
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        )
        # browser.set_verbose(2)

        browserOpened = False
        count = 0
        while browserOpened is False:
            if len(self.proxies) < 1 or count >= 3:
                if len(self.proxies) > 0 and self.proxy is not None:
                    appProxyHandler = AppProxyHandler()
                    appProxyHandler.inactiveProxy(self.proxy)

                guiElem.setText("Settting new proxy")
                self.setProxy()
                count = 0

            try:
                browser.session.proxies = self.proxies
                browser.open(url)
                if re.search('This IP has been automatically blocked', str(browser.get_current_page())):
                    guiElem.setText("Proxy blocked")
                    appProxyHandler = AppProxyHandler()
                    appProxyHandler.inactiveProxy(self.proxy)
                    guiElem.setText("Setting new proxy")
                    self.setProxy()
                    browserOpened = False
                    count = 0

                browser.select_form('.picker')
                if len(browser.get_current_page().find_all('input', attrs={"name": "id"})) > 0:
                    browser["id"] = val
                elif len(browser.get_current_page().find_all('input', attrs={"name": "n"})) > 0:
                    browser["n"] = val
                resp = browser.submit_selected()

                browserOpened = True

            except ConnectionError:
                time.sleep(1)
                count += 1
                guiElem.setText("Proxy failed #"+str(count))
                continue

        return browser.get_url()


    def setProxy(self):
        appProxyHandler = AppProxyHandler()
        self.proxy = appProxyHandler.getProxy()

        self.proxies = {
            "http": self.proxy.type+"://"+self.proxy.ip+":"+self.proxy.port,
            "https": self.proxy.type+"://"+self.proxy.ip+":"+self.proxy.port
        }
