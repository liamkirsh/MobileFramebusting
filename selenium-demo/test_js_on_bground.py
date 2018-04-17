import os
from selenium import webdriver

__location__ = os.path.realpath(os.getcwd())
driver = webdriver.Chrome(os.path.join(__location__, "chromedriver"))
driver.get("file:///home/liam/Documents/14-828/MobileFramebusting/selenium-demo/empty.html")
driver.execute_script('\
var newframe = document.createElement("iframe"); newframe.id = "myframe"; newframe.src = "http://example.com"; document.body.appendChild(newframe)')

print driver.find_elements_by_id("myframe")[0]
driver.switch_to.frame(driver.find_elements_by_id("myframe")[0])
driver.switch_to.frame(driver.find_elements_by_id("myframe")[0])
print driver.execute_script('return document.URL')
# driver.switch_to.default_content()
