import json
import re
import time
import sys

import requests
from bs4 import BeautifulSoup

from appProxyHandler import AppProxyHandler
from clFormSubmitter import ClFormSubmitter
from newProfileDialog import Ui_newProfileDialog


class ClPageScrapper:
    proxies = {}

    locationUrl = "https://www.craigslist.org/about/sites"

    def __init__(self):
        self.clFormSubmitter = ClFormSubmitter()

    # to get craigslist location data
    def getClLocationData(self, guiElem):
        soup = self.getSoup(self.locationUrl, guiElem)
        selectedHtml = soup.section

        locationUrlDict = {}

        try:
            colmaskDivArr = selectedHtml.find_all("div", class_='colmask')
        except AttributeError:
            return json.dumps(locationUrlDict)

        for colmaskDivHtml in colmaskDivArr:
            boxDivArr = colmaskDivHtml.find_all("div", class_='box')
            for boxDivHtml in boxDivArr:
                boxH4Arr = boxDivHtml.find_all('h4')
                boxUlArr = boxDivHtml.find_all('ul')
                for i in range(len(boxH4Arr)):
                    boxUlLiArr = boxUlArr[i].find_all('li')
                    subLocationUrlList = []
                    for boxUlLiHtml in boxUlLiArr:
                        subLocationUrlDict = {'location': boxUlLiHtml.find('a').text,
                                              'link': boxUlLiHtml.find('a')['href']}
                        subLocationUrlList.append(subLocationUrlDict)

                    locationUrlDict[boxH4Arr[i].text] = subLocationUrlList

        return json.dumps(locationUrlDict)



    def getClPostLink(self, url, guiElem):
        soup = self.getSoup(url, guiElem)
        try:
            selectedHtml = soup.find('li', class_='post')
            postAnchorHtml = selectedHtml.find('a')
        except AttributeError:
            return ""

        return postAnchorHtml['href']



    def getClPostTypes(self, url, guiElem):
        guiElem.setText("Getting post link")
        postLink = self.getClPostLink(url, guiElem)

        if postLink != "":
            guiElem.setText("Scrapping post type")
            soup = self.getSoup(postLink, guiElem)
            try:
                pickerFormHtml = soup.find('form', class_='picker')
            except ArithmeticError:
                pickerFormHtml = ""

            if pickerFormHtml is not None:
                formActionLink = pickerFormHtml['action']
                formInputLabelHtmlArr = pickerFormHtml.find_all("label")

                clPostTypeDict = {}
                for formInputLabelHtml in formInputLabelHtmlArr:
                    formInputHtml = formInputLabelHtml.find("input", attrs={"name": "id"})
                    formLabelText = formInputLabelHtml.text
                    clPostTypeDict[formInputHtml['value']] = re.sub(r'[\n\r\t]*', '', formLabelText).lstrip()

                return json.dumps({"postPageLink":postLink, "formActionLink":formActionLink, "clPostTypeDict":clPostTypeDict})
            else:
                return json.dumps({})
        else:
            return json.dumps({})



    def getClPostPickerFormData(self, formVal, currentUrl, guiElem):
        newUrl = self.clFormSubmitter.clPostPickerFormSubmit(currentUrl, formVal, guiElem)

        soup = self.getSoup(newUrl, guiElem)
        try:
            formHtml = soup.find('form', class_='picker')
        except ArithmeticError:
            return False

        if formHtml is not None:
            formActionLink = formHtml['action']
            formInputLabelHtmlArr = formHtml.find_all("label")

            clPostFormDataDict = {}
            for formInputLabelHtml in formInputLabelHtmlArr:
                # formInputHtml = formInputLabelHtml.find("input", attrs={"name": "id"})
                formInputHtml = formInputLabelHtml.find("input")
                formLabelText = formInputLabelHtml.text
                clPostFormDataDict[formInputHtml['value']] = re.sub(r'[\n\r\t]*', '', formLabelText).lstrip()

            return json.dumps(
                {"postPageLink": newUrl, "formActionLink": formActionLink, "clPostFormDataDict": clPostFormDataDict}
            )
        else:
            return False



    # to get html soup from reference url
    def getSoup(self, refUrl, guiElem):
        page = ''
        count = 0
        while page == '':
            if len(self.proxies) < 1 or count >= 3:
                if len(self.proxies) > 0 and self.proxy is not None:
                    appProxyHandler = AppProxyHandler()
                    appProxyHandler.inactiveProxy(self.proxy)

                guiElem.setText("Settting new proxy")
                self.setProxy()
                count = 0

            try:
                page = requests.get(refUrl, proxies=self.proxies)
            except requests.ConnectionError:
                time.sleep(1)
                count += 1
                guiElem.setText("Proxy failed #"+str(count))
                continue

            if re.search('This IP has been automatically blocked', page.text):
                guiElem.setText("Proxy blocked")
                appProxyHandler = AppProxyHandler()
                appProxyHandler.inactiveProxy(self.proxy)
                guiElem.setText("Setting new proxy")
                self.setProxy()
                page = ''
                count = 0

        soup = BeautifulSoup(page.content, 'html.parser')
        return soup


    def setProxy(self):
        appProxyHandler = AppProxyHandler()
        self.proxy = appProxyHandler.getProxy()

        self.proxies = {
            "http": self.proxy.type+"://"+self.proxy.ip+":"+self.proxy.port,
            "https": self.proxy.type+"://"+self.proxy.ip+":"+self.proxy.port
        }
