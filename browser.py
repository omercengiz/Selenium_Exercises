from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

class Browser:
    def __init__(self,link):
        self.link = link
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        Browser.redirectInstagram(self)


    def redirectInstagram(self):

        self.browser.get(self.link)
        time.sleep(2)
        Browser.login(self)
        Browser.getFollowers(self)

    def login(self):
        username = self.browser.find_element_by_name("username")
        password = self.browser.find_element_by_name("password")

        username.send_keys("your_username")
        password.send_keys("12345")


        loginBtn = self.browser.find_element_by_css_selector("#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child(4)")
        loginBtn.click()
        time.sleep(5)
        self.browser.get(self.link)

    def getFollowers(self):
        followers_link = self.browser.find_element_by_css_selector("#react-root > section > main > div > header > section > ul > li:nth-child(2) > a")
        followers_link.click()
        time.sleep(4)

        Browser.scrollDown(self)

        followers = self.browser.find_elements_by_css_selector(".FPmhX.notranslate._0imsa")
        for i in followers:
            print(i.text)


    def scrollDown(self):
        scroll_Down ="""
        page = document.querySelector(".isgrP");
        page.scrollTo(0,page.scrollHeight);
        var EndPage = page.scrollHeight;
        return EndPage;
        """

        EndPage = self.browser.execute_script(scroll_Down)

        while True:
            ending_page = EndPage
            time.sleep(1)
            EndPage = self.browser.execute_script(scroll_Down)
            if ending_page == EndPage:
                break