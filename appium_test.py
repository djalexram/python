import unittest
from browsermobproxy import Server   
from filter import Harfilter
from sel import Setup,Player
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import Proxy, ProxyType 
#from selenium import webdriver
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

import ast
import json
import time
import sel

class wait_for_index_to_change():

    def __call__(self, driver):
        try:
            index = driver.execute_script(sel.js_getIndex)
            return int(index) > 0
        except TimeoutException:
            return False



class MobileNextSlates(unittest.TestCase):
	def setUp(self):
	 	#self.server = Server(sel.browsermob_path,options={'port': 9091})
	 # 	self.server = Server(sel.browsermob_path)
	 # 	self.server.start()
	 # 	self.proxy = self.server.create_proxy()
	 # 	print self.proxy.selenium_proxy().httpProxy
	 # 	prox = Proxy()
		# prox.proxy_type = ProxyType.MANUAL
		# prox.http_proxy = self.proxy.selenium_proxy().httpProxy
		# prox.socks_proxy = self.proxy.selenium_proxy().httpProxy
		# prox.ssl_proxy = self.proxy.selenium_proxy().sslProxy
		# prox.autodetect = False

	 	#capabilities = { 'platformName': 'Android', 'platformVersion': '4.4.2','deviceName': 'Android Emulator','browserName': 'Chrome', 'app': sel.chrome_apk}
	 	#capabilities = { 'platformName': 'Android', 'platformVersion': '5.0.2','deviceName': 'Andriod','udid':'33000da9236e32ab','browserName': 'Chrome'}
	 	capabilities = { 'automationName':'XCUITest','platformName': 'iOS', 'platformVersion': '9.3','deviceName': 'iPad','browserName': 'safari'}
	 	#capabilities = { 'automationName':'XCUITest','platformName': 'iOS', 'platformVersion': '9.3.5','deviceName': 'iPad','browserName': 'safari','udid':'2c7ed32cfd5b704d079ba490c87893be1ee2e249',"xcodeOrgId": "developer ID", "xcodeSigningId": "iPhone Developer"}
	 	
	 	#capabilities = { 'automationName': 'Appium', 'platformName': 'Android', 'platformVersion': '4.4.2','deviceName': 'Android Emulator', 'autoWebview':'true',  'app': 'com.android.chrome','appPackage': 'com.android.chrome','appActivity': 'com.android.chrome.ChromeTabbedActivity'}
		#prox.add_to_capabilities(capabilities)
		#self.proxy.new_har("player",options = {"captureHeaders": True, "captureContent": True, "captureBinaryContent": False})
		self.driver = webdriver.Remote('http://localhost:4723/wd/hub', capabilities)

	 	self.driver.get(sel.appium_url)

	def test_click_start_next_slate(self):
		if len(self.driver.find_elements_by_id(sel.chrome_termsID)) > 0:
			self.driver.find_element_by_id(sel.chrome_termsID).click()
		#print self.driver.contexts
		#self.driver.switch_to.context(self.driver.contexts[0])
	
		player = self.driver.execute_script(sel.js_player_type)
		print player
		if player== "kmc":
			self.driver.switch_to_frame(sel.kmc_frame)
		bc_ver= self.driver.execute_script(sel.js_bc_v)
		if bc_ver:
			print "Player version: " + str(bc_ver)
			mute= sel.bc_mute
		time.sleep(3)
		#if len(self.driver.find_elements_by_css_selector(sel.bc_play)) > 0:
		# el = self.driver.find_element_by_css_selector(sel.bc_play)
		# action = TouchAction(self.driver)
		# action.tap(el).perform()
		self.driver.find_element_by_xpath(sel.bc_play).click()
		current = self.driver.execute_script(sel.js_getIndex)
		player = Player(self.driver)
		player.click_start_next_slate()
		time.sleep(3)
		next = self.driver.execute_script(sel.js_getIndex)
		time.sleep(3)
		
		assert current != next, "Javascript player index did not increment"
	

	def click_end_next_slate(self):
		if len(self.driver.find_elements_by_id(sel.chrome_termsID)) > 0:
			self.driver.find_element_by_id(sel.chrome_termsID).click()
		#print self.driver.contexts
		#self.driver.switch_to.context(self.driver.contexts[0])
	
		player = self.driver.execute_script(sel.js_player_type)
		print player
		if player== "kmc":
			self.driver.switch_to_frame(sel.kmc_frame)
		bc_ver= self.driver.execute_script(sel.js_bc_v)
		if bc_ver:
			print "Player version: " + str(bc_ver)
			mute= sel.bc_mute
		if len(self.driver.find_elements_by_css_selector(sel.bc_play)) > 0:
			self.driver.find_element_by_css_selector(sel.bc_play).click()
		element = self.driver.find_element_by_xpath(mute)
		self.driver.execute_script("$(arguments[0]).click();", element)
		current = self.driver.execute_script(sel.js_getIndex)
		player = Player(self.driver)
		player.click_end_next_slate()
		time.sleep(3)
		next = self.driver.execute_script(sel.js_getIndex)
		time.sleep(3)
		
		assert current != next, "Javascript player index did not increment"




	def tearDown(self):
	# close the browser window
		self.driver.quit()
		#self.server.stop()

if __name__ == '__main__':
    unittest.main(verbosity=2)