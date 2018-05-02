import sys
import os
import glob
import unittest
import time
import json
from pprint import pprint

from appium import webdriver
#from appium import logging
# import org.openqa.selenium.chrome.ChromeDriver;

PLATFORM_VERSION = '7.0'
appium_URL = 'http://localhost:4723/wd/hub'
# 'http://appium.com/';
screenshot_path = '/home/bdavs/Pictures/chrome';

logFile = open("mobileHeaders.csv","w+")

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
            'perfLoggingPrefs': {"enableNetwork": "true",
                                 "enablePage": "false" },
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

#        self.driver.implicitly_wait(10)
#        self.driver.set_page_timeout(10)
#        self.driver.set_script_timeout(10)
        self.driver.set_page_load_timeout(10)
        try:
            domains = open("top-100.txt", 'r')
        except IOError:
            sys.stderr.write("Error opening input domain list \n")
            sys.exit(1)

        for rank, domain in enumerate(domains):
            try:
                url = "http://" + domain.strip()
                log(str(rank) + ":  " +url)
                logString=url
    #            log ("Loading page")
    #            self.driver.get("https://bitbar.com/testing")
                self.driver.get(url)

            except:
                log(url + ": ERROR restarting and moving on\n")
                logFile.write(url + ": ERROR\n")
                self.retry()
                self.setUp()


            try:
                log("Screenshotting")
                self.driver.save_screenshot(screenshot_path + "/" + domain + ".png")
                
                log("getting logs")
                #logs = self.driver.current_url
                logs = self.driver.get_log("performance")
                mobileURL=self.driver.current_url
                for entry in logs:
                    xfo=""
                    csp=""

                    if('message' in entry):
#                        pprint(entry['message'])
                        if('message' in entry['message']):
                            jsondata = json.loads(entry['message'])
                            if(jsondata['message']['method'] == "Network.responseReceived"):
                                if('parentFrameId' in jsondata['message']['params']):
#                                    print(jsondata['message']['params'])
                                    continue
                                if('type' in jsondata['message']['params']):
                                    if(jsondata['message']['params']['type'] != 'Document'):
                                        continue
                                if('x-frame-options' in jsondata['message']['params']['response']['headers']):
                                    xfo = jsondata['message']['params']['response']['headers']['x-frame-options']
                                if('content-security-policy' in jsondata['message']['params']['response']['headers']):
                                    csp = jsondata['message']['params']['response']['headers']['content-security-policy']

                                logString=url+",,,"+mobileURL+","+xfo+","+csp
                                logFile.write(logString+'\n')
                                logFile.flush()
                                break
                            #type(entry['message']))
#                            print(entry['message'].keys())
#                            pprint(entry['message']['message'])
#                    pprint(entry)

                
           # log(str(logs))
#                jsontemp = json.dumps(logs)
                #logFile.write(logString+'\n')
                #logFile.flush()
            except:
                logFile.flush()
                log("error moving on")


        log("completed")
#        log ("Loading next page")
#        self.driver.get("https://google.com")

#        log("getting next logs")
#        logs = self.driver.get_log("performance")
        #log(str(logs))

#        self.logFile.write("google: "+str(logs)+" \n")

#        log(self.driver.logs.get("performance"))
#2        log ("Taking screenshot of home page: '1_home.png'")

    def retry(self):
        self.driver.quit()
    def tearDown(self):
        logFile.close()
        self.driver.quit()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AndroidWebViewTests)
    unittest.TextTestRunner(verbosity=1).run(suite)
