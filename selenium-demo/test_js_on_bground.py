import os
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

__location__ = os.path.realpath(os.getcwd())

class frame_JS_to_be_available_and_switch_to_it:
    def __init__(self, locator):
        self.locator = locator
    def __call__(self, driver):
        driver.switch_to.frame(self.locator)
        return not driver.execute_script('return self === top')

driver = webdriver.Chrome(os.path.join(__location__, "chromedriver"))
driver.get("file:///home/liam/Documents/14-828/MobileFramebusting/selenium-demo/empty.html")
driver.execute_script('\
var newframe = document.createElement("iframe"); newframe.id = "myframe"; newframe.src = "http://example.com"; document.body.appendChild(newframe)')
wait = WebDriverWait(driver, 10).until(frame_JS_to_be_available_and_switch_to_it("myframe"))
print driver.execute_script('return document.URL')
# driver.switch_to.default_content()
