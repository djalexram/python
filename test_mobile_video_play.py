import pytest 
from sel import Player,wait_for_video_to_change, wait_for_first_video,wait_for_page_load
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

	def test_video_play(self,selenium,mobile,browser,preroll_ads,player_num,skip_forward_present):
		driver = selenium
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
	 		if next_plat:
	 			playlist = player.get_playlist_len()
	 		else:
	 			playlist = 5
	 		videos_played = []
	 		for x in range(1,playlist):
	 			player.wait_for_ad()
	 			temp = player.get_first_video()
	 			if temp and temp not in videos_played:
	 				videos_played.append(temp)
	 			player.scrub()
	 			element = WebDriverWait(driver, max_timeout).until(
	 				wait_for_video_to_change(player_num)
	 			)
	 			time.sleep(2)
	 		print "Videos played: " + str(len(videos_played))

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
	
