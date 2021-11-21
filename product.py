from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class product:
    def __init__(self, name, url):
        self.m_url = url
        print(url, end=":\n")
        # get which websites we are using
        self.m_website = getUrlWebsite(url)
        print("\twebsite: " + self.m_website)
        # get product id
        self.m_id = self.processUrl()
        print("\tid: " + self.m_id)
        self.m_url = websites[self.m_website] + self.m_id
        if name == "":
            # if no name was given, get name from website
            self.m_name = self.getUrlName()
        else:
            self.m_name = name
        print("\tname: " + self.m_name)
        self.avaliable = False
        self.stat = ""

    # websiteIDDict contains different function pointers for getting product id
    # it's a dictionary, key values are website
    def processUrl(self):
        return websitesIDDict[self.m_website](self.m_url)

    # get the product name from website
    def getUrlName(self):
        # init driver
        m_driver = webdriver.Chrome("C:\\Users\\Zeke\\Root\\Program Files\\chromedriver_win32\\chromedriver.exe",
                                    chrome_options=chromeOptions)
        # websiteNameDict contains different function pointers for getting product name
        # it's a dictionary, key values are website
        ret = websitesNameDict[self.m_website](m_driver, self.m_id)
        m_driver.close()
        m_driver.quit()
        return ret

    # get the product status for this product
    def getStat(self):
        stat = []
        # init driver
        m_driver = webdriver.Chrome("C:\\Users\\Zeke\\Root\\Program Files\\chromedriver_win32\\chromedriver.exe",
                                    chrome_options=chromeOptions)
        # websiteStatDict contains different function pointers for getting product stat
        # it's a dictionary, key values are website
        for item in websitesStatDict[self.m_website](m_driver, self.m_id):
            stat.append(item)
            if item == "Available to ship" or item == "Available for free store pickup" or item == "In Stock":
                self.avaliable = True

        m_driver.close()
        m_driver.quit()
        self.stat = [str(self.m_name), str("/".join(i for i in stat)), str(self.m_url)]
        return self.stat

    def toString(self):
        return self.m_name + " Available as: " + self.stat[1]


# checking the front of the url, to decided which website it is
def getUrlWebsite(url):
    if url.startswith("https://www.bestbuy."):
        return 'bestbuy'
    elif url.startswith("https://www.amazon."):
        return 'amazon'


# getting product stat from BestBuy
def getBestBuyStat(m_driver, m_id):
    # websites is a dictionary containing url for each website
    # it's a dictionary, key values are website
    m_driver.get(websites['bestbuy'] + m_id)
    m_driver.implicitly_wait(5)
    # get text inside of these two elem, one shipping stat, one is in-store stat
    return getClassElementText(m_driver, ['availabilityMessage_ig-s5 container_1DAvI', 'availabilityMessageTitle_3Qo22'])


# getting product name from BestBuy
def getBestBuyName(m_driver, m_id):
    m_driver.get(websites['bestbuy'] + m_id)
    m_driver.implicitly_wait(5)
    # execute java script to get the product name
    return m_driver.execute_script('return document.getElementsByClassName("productName_3nyxM")[0].textContent')


# getting product id from BestBuy, at the end of the url
def getBestBuyID(url):
    return url.split("/")[-1]


# getting product stat from Amazon
def getAmazonStat(m_driver, m_id):
    m_driver.get(websites['amazon'] + m_id)
    m_driver.implicitly_wait(5)
    ret = []
    # get text inside of these two elem, one shipping stat, one is in-store stat
    availability = getIDElementText(m_driver, ['availability'])[0].replace("\n", "")
    if 'in stock.' in availability.lower():
        ret.append(availability)
    else:
        ret.append("Not available")
    return ret


# getting product name from Amazon
def getAmazonName(m_driver, m_id):
    m_driver.get(websites['amazon'] + m_id)
    m_driver.implicitly_wait(5)
    # execute java script to get the product name
    return m_driver.execute_script('return document.getElementById("productTitle").textContent').replace("\n", "")


# getting product id from Amazon, which is after /dp/
def getAmazonID(url):
    arr = url.split("/")
    for idx, item in enumerate(arr):
        if item == "dp":
            return arr[idx + 1]


# get text from html, using class name to find
def getClassElementText(driver, classNames):
    ret = []
    for className in classNames:
        ret.append(driver.execute_script('return document.getElementsByClassName("' + className + '")[0].textContent'))
    return ret


# get text form html, using id to find
def getIDElementText(driver, ids):
    ret = []
    for id in ids:
        ret.append(driver.execute_script('return document.getElementById("' + id +  '").textContent'))
    return ret


websites = {
    'bestbuy': 'https://www.bestbuy.ca/en-ca/product/',
    'amazon': 'https://www.amazon.ca/dp/'
}
websitesStatDict = {
    'bestbuy': getBestBuyStat,
    'amazon': getAmazonStat
}
websitesNameDict = {
    'bestbuy': getBestBuyName,
    'amazon': getAmazonName
}
websitesIDDict = {
    'bestbuy': getBestBuyID,
    'amazon': getAmazonID
}


chromeOptions = Options()
chromeOptions.add_argument('blink-settings=imagesEnabled=false')
chromeOptions.add_argument('--disable-plugins')
chromeOptions.add_argument('--disable-javascript')
chromeOptions.add_argument('--incognito')
chromeOptions.add_argument("--disable-gpu");
chromeOptions.add_argument("--disable-extensions");