import os
import glob
import unittest
import time

from appium import webdriver
# import org.openqa.selenium.chrome.ChromeDriver;

PLATFORM_VERSION = '7.0'
appium_URL = 'http://localhost:4723/wd/hub'
# 'http://appium.com/';
screenshot_path = '/home/bdavs/Pictures/chrome';



def log(msg):
        print (time.strftime("%H:%M:%S") + ": " + msg)

class AndroidWebViewTests(unittest.TestCase):

    def setUp(self):

        desired_caps = {
            'platformName': 'Android',
            'platformVersion': PLATFORM_VERSION,
            'deviceName': 'AndroidDevice',
            'browserName': 'chrome',
            'enablePerformanceLogging': 'true',
            'loggingPrefs': { "browser": "ALL" }
        }

 #       if (PLATFORM_VERSION < '4.4'):
 #           desired_caps['automationName'] = 'selendroid'

        log ("WebDriver request initiated. Waiting for response, this may take a while.")

        self.driver = webdriver.Remote(appium_URL,
                                       desired_caps)

    
    def test_webview(self):

#        log ("Taking screenshot of home page: '0_chromeLaunched.png'")
#        self.driver.save_screenshot(screenshot_path + "/0_chromeLaunched.png")

        log ("Loading page")
        self.driver.get("https://bitbar.com/testing")

#        log("getting log types")
#        temp = self.driver.log_types
#        log(str(temp))

        log("getting logs")
 #       logs = self.driver.get_log("browser")
 #       log(str(logs))

        logs = self.driver.get_log("performance")
        log(str(logs))

 #       log("trying script")
 #       time.sleep(5)
 #       timings = self.driver.execute_script("return window.performance.getEntries();")
 #       log( str(timings))
        
#        log(self.driver.logs.get("performance"))
#2        log ("Taking screenshot of home page: '1_home.png'")
#        self.driver.save_screenshot(screenshot_path + "/1_home.png")

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AndroidWebViewTests)
    unittest.TextTestRunner(verbosity=1).run(suite)
