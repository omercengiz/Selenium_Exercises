from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager


class Browser:
    def __init__(self, username=None, password=None):
        assert username is not None, "Username has not been provided."
        assert password is not None, "Password has not been provided."

        self.login_link = "https://www.instagram.com/accounts/login/?source=auth_switcher"
        self.homepage_link = "https://www.instagram.com/"
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.implicitly_wait(5)
        Browser._redirect_instagram(self)

    def _redirect_instagram(self):
        self.driver.get(self.login_link)
        Browser._login(self)

        try:
            self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
        except:
            pass

        Browser._get_followers(self)

    def _login(self):
        username_section = self.driver.find_element_by_name("username")
        password_section = self.driver.find_element_by_name("password")

        username_section.send_keys(self.username)
        password_section.send_keys(self.password)

        login_button = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')
        login_button.click()

        # wait explicitly 5 seconds until the top bar is appeared..!
        WebDriverWait(self.driver, 5).until(
            ec.presence_of_element_located(
                (By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div')
            )
        )

        self.driver.get(self.homepage_link + self.username)

    def _get_followers(self):
        followers_popup = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'
        )
        followers_popup.click()
        Browser._scroll_down(self)

        followers = self.driver.find_elements_by_css_selector(".FPmhX.notranslate._0imsa")
        for follower in followers:
            print(follower.text)

    def _scroll_down(self):
        # breakpoint()
        # TODO scrollTo down part doesn't work properly all the time. Maintain!!
        scroll_down_script = """
        page = document.querySelector(".isgrP");
        page.scrollTo(0,page.scrollHeight);
        var EndPage = page.scrollHeight;
        return EndPage;
        """
        end_page = self.driver.execute_script(scroll_down_script)

        while True:
            print(end_page)
            temp = end_page
            end_page = self.driver.execute_script(scroll_down_script)

            if temp == end_page:
                break
