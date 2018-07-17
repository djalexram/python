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

	def test_start_next_slate(self,selenium,mobile,browser,preroll_ads,player_num,skip_forward_present):
		driver = selenium
	 	try:
	 		if browser == "andriod" and len(driver.find_elements_by_id(sel.chrome_termsID)) > 0:
	 			driver.find_element_by_id(sel.chrome_termsID).click()
	 		player = Player(driver,timeout,preroll_ads,player_num)
	 		player.check_if_paused()
	 		player.wait_for_ad()
	 		url = driver.current_url
	 		og_plat = player.get_current_platformID()
	 		next_plat = False
	 		if stage_url in url:
	 			for x in range (1,15):
	 				print "waiting for watch call"
	 				time.sleep(2)
	 				next_plat = player.get_playlist_platformID(2)
	 				if next_plat:
	 					break
			player.click_forward()
			player.wait_for_ad()
			player.check_if_paused()
			v1 = player.get_first_video()
			if next_plat:
				index = int(player.get_currentIndex()) +1
			print "Waiting for start next slate to appear"
			text = player.get_start_next_slate()
			print "Start next slate text: " + text
			player.wait_for_ad()
			v2 = player.get_first_video()
			if next_plat:
				print "Expected platformID: " + next_plat
				assert player.get_playlist_platformID(index) == player.get_current_platformID(), "Expected platform id does not match with current"
			else:
				assert v1 != v2
		
		
	 	except AssertionError:
			raise

		except:
			driver.save_screenshot(sel.get_screenshot_filename(path))
			raise
		
		finally:
			player = Player(driver,timeout,preroll_ads,player_num)
			player.get_js_api_calls()

	def test_end_next_slate(self,selenium,mobile,browser,preroll_ads,player_num,skip_forward_present):
		driver = selenium
	 	try:
	 		if browser == "andriod" and len(driver.find_elements_by_id(sel.chrome_termsID)) > 0:
	 			driver.find_element_by_id(sel.chrome_termsID).click()
	 		player = Player(driver,timeout,preroll_ads,player_num)
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
			print "Waiting for end next slate to appear"
			player.scrub()
			text = player.get_end_next_slate(max_timeout)
			print "End next slate text: " + text
			player.wait_for_ad()
			v2 = player.get_first_video()
			if next_plat:
				print "Expected platformID: " + next_plat
				assert next_plat == player.get_current_platformID(), "Expected platform id does not match with current"
			else:
				assert v1 != v2
		
	 	except AssertionError:
			raise

		except:
			driver.save_screenshot(sel.get_screenshot_filename(path))
			raise
		
		finally:
			player = Player(driver,timeout,preroll_ads,player_num)
			player.get_js_api_calls()
			cookies = driver.get_cookies()
			if cookies:
				cookie = player.get_iris_cookie(cookies)
				if cookie:
					print str(cookie)
	
