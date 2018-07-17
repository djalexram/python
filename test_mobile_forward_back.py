import pytest
from sel import Player
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from appium.webdriver.common.touch_action import TouchAction

import ast
import json
import time
import sel


@pytest.mark.mobile
@pytest.mark.noproxy
class TestVideoPlay(object):

	def test_click_forward(self,mobile,browser,selenium,preroll_ads,player_num,skip_forward_present):
		driver = selenium
		#adb logcat | grep -i "console"
	 	#capabilities = { 'platformName': 'Android', 'platformVersion': '4.4.2','deviceName': 'Android Emulator','browserName': 'Chrome', 'app': sel.chrome_apk}
	 	#capabilities = { 'platformName': 'Android', 'platformVersion': '5.0.2','deviceName': 'Andriod','udid':'33000da9236e32ab','browserName': 'Chrome'}
	 	#capabilities = { 'automationName':'XCUITest','platformName': 'iOS', 'platformVersion': '9.3','deviceName': 'iPad','browserName': 'safari'}
	 	#capabilities = { 'automationName':'XCUITest','platformName': 'iOS', 'platformVersion': '9.3.5','deviceName': 'iPad','browserName': 'safari','udid':'2c7ed32cfd5b704d079ba490c87893be1ee2e249',"xcodeOrgId": "developer ID", "xcodeSigningId": "iPhone Developer"}
	 	
	 	#capabilities = { 'automationName': 'Appium', 'platformName': 'Android', 'platformVersion': '4.4.2','deviceName': 'Android Emulator', 'autoWebview':'true',  'app': 'com.android.chrome','appPackage': 'com.android.chrome','appActivity': 'com.android.chrome.ChromeTabbedActivity'}
	

	 	try:
	 		if browser == "andriod" and len(driver.find_elements_by_id(sel.chrome_termsID)) > 0:
	 			driver.find_element_by_id(sel.chrome_termsID).click()
	 		player = Player(driver,timeout,preroll_ads,player_num)
	 		#touch.tap(play).perform()
	 		player.check_if_paused()
	 		player.wait_for_ad()
	 		url = driver.current_url
	 		og_plat = player.get_current_platformID()
	 		next_plat = False
	 		if stage_url in url:
	 			for x in range (1,15):
	 				print "waiting for watch call"
	 				time.sleep(2)
	 				next_plat = player.get_playlist_platformID(1)
	 				if next_plat:
	 					break
	 		v1 = player.get_first_video()
	 		player.click_forward()
	 		#action = TouchAction(driver)
	 		#action.move_to(None, 284, 287).wait(200).tap(None, 284, 287, 1).perform()
	 		player.wait_for_ad()
	 		player.check_if_paused()
	 		v2 = player.get_first_video()
	 		time.sleep(3)
	 		if next_plat:
				print "Expected platformID: " + next_plat
				assert next_plat == player.get_current_platformID(), "Skip forward is not working"
				preIndex = int(player.get_currentIndex()) -1
			else:
				assert v1 != v2
			player.click_back()
			player.wait_for_ad()
			v3 = player.get_first_video()
			if next_plat:
				assert player.get_playlist_platformID(preIndex) == player.get_current_platformID(), "Skip back is not working"
			else:
				assert v1 == v3
		

	 	except AssertionError:
			raise

		except:
			driver.save_screenshot(sel.get_screenshot_filename(path))
			raise
		
		finally:
			player = Player(driver,timeout,preroll_ads,player_num)
			tags = player.get_js_api_calls()
			player.get_query_strings(tags)
			cookies = driver.get_cookies()
			if cookies:
				cookie = player.get_iris_cookie(cookies)
				if cookie:
					print str(cookie)
