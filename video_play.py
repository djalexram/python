import unittest
from browsermobproxy import Server   
from filter import Harfilter
from sel import Setup,Player,wait_for_video_to_change, wait_for_first_video,wait_for_page_load,Headless, headless, max_timeout
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locators import PlayerLocators
from selenium import webdriver
from ddt import ddt, data, file_data
from pyvirtualdisplay import Display

import ast
import json
import time
import sel

@ddt
class VideoPlay(unittest.TestCase):
	def setUp(self):
		sel.page_load_timeout = True
		self.browser = sel.browser
		self.server = Server(sel.browsermob_path)
		self.server.start()
		self.proxy = self.server.create_proxy()
		if headless:
			self.head = Headless()
			self.display = self.head.start()
		self.setup = Setup()
		self.driver = self.setup.browser(self.proxy.selenium_proxy().httpProxy,self.proxy.selenium_proxy().sslProxy)
		self.proxy.new_har("player",options = {"captureHeaders": True, "captureContent": True, "captureBinaryContent": False})

	@file_data(sel.urls_path)
	def test_video_play(self,url):
		try:
			self.driver = self.setup.player(url)
			if sel.player == "vdb":
				print "waiting for player bar to load"
				element = WebDriverWait(self.driver, sel.timeout).until(
					EC.presence_of_element_located((PlayerLocators.VDB_PLAYER_BAR))
					)
			player = Player(self.driver)
			if sel.skip_forward_present:
				player.wait_for_forward()
			player.wait_for_ad()
			url = self.driver.current_url
			if ".nfl." in url:
				checkbox_list = self.driver.find_elements(*PlayerLocators.NFL_ENABLE_IRIS)
				if len(checkbox_list) > 0:
					checkbox_list[0].click()
					print "click checkbox"
			filter = Harfilter(self.proxy.har)
			watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
			if len(watch_list) == 0:
				print "waiting for first watch call"
				time.sleep(10)
				filter = Harfilter(self.proxy.har)
				watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
				if len(watch_list) == 0:
					print "waiting for first watch call"
					time.sleep(15)
					filter = Harfilter(self.proxy.har)
					watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
			if len(watch_list) >=1:
				watch_success = sel.check_single_response(watch_list)
				print "\nWatch call response: \n" + str(json.dumps(sel.get_json(watch_list), ensure_ascii=True))
				rec_len = sel.get_playlist_length(watch_list)
				print "\nTotal initial asset list: " + str(rec_len)
				if rec_len in range(1,4):
					print "WARN: Watch call has less than 4 assets"
			if not player.get_first_video():
				element = WebDriverWait(self.driver, sel.timeout).until(
					wait_for_first_video()
					)
			#player.click_end_next_slate()
			filter = Harfilter(self.proxy.har)
			iris_files = filter._filter_return_iris_files(sel.iris_path)
			httpErrors = filter._filter_check_all_errors(sel.iris_path)
			assert len(httpErrors) == 0, "Some files failed to load due to HTTP errors"
			if '.js' not in sel.check_iris_files(iris_files):
				print "Iris JS file missing\n"
			print "\nWaiting for video to finish playing and autoplay next asset"
			for x in range(1,4):
				player.get_first_video()
				element = WebDriverWait(self.driver, sel.max_timeout).until(
					wait_for_video_to_change()
					)
				time.sleep(2)
			filter = Harfilter(self.proxy.har)
			watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
			watch_calls =  filter.get_matches(sel.iris_watch)
			update_calls =  filter.get_matches(sel.iris_update)
			next_calls =  filter.get_matches(sel.iris_next)
			watch_qstrings = filter._filter_return_request_querystring(sel.iris_watch)
			update_qstrings = filter._filter_return_request_querystring(sel.iris_update)
			next_qstrings = filter._filter_return_request_querystring(sel.iris_next)
			sel.get_watch_calls(watch_qstrings)
			sel.get_next_calls(next_qstrings)
			sel.get_update_calls(update_qstrings)
			sel.total_calls(watch_calls,update_calls,next_calls)
			platform_id_update = sel.check_platform_id(update_qstrings)
			platform_id_next = sel.check_platform_id(next_qstrings)
			apiErrors = filter._filter_check_all_errors(sel.iris_api)
			assert platform_id_update== 0, "There was " + str(platform_id_update) + " update calls missing platform_id"
			assert platform_id_next== 0, "There was " + str(platform_id_next) + " next calls missing platform_id"
			assert watch_success == True, "success did not equal true in watch call response"
			percent_watched = sel.get_percentage_watched(update_qstrings)
			
			assert len(watch_calls) > 0, "No watch calls logged"
			assert len(watch_calls) == sel.expected_watch, "Extra watch calls: " + str(len(watch_calls)-1)
			assert len(apiErrors) == 0, "Some API calls failed due to HTTP errors"
			
		except AssertionError:
			self.driver.quit()
			self.server.stop()
			raise

		except:
			filter = Harfilter(self.proxy.har)
			watch_calls =  filter.get_matches(sel.iris_watch)
			update_calls =  filter.get_matches(sel.iris_update)
			next_calls =  filter.get_matches(sel.iris_next)
			watch_qstrings = filter._filter_return_request_querystring(sel.iris_watch)
			update_qstrings = filter._filter_return_request_querystring(sel.iris_update)
			next_qstrings = filter._filter_return_request_querystring(sel.iris_next)
			sel.get_watch_calls(watch_qstrings)
			sel.get_update_calls(update_qstrings)
			sel.get_next_calls(next_qstrings)
			apiErrors = filter._filter_check_all_errors(sel.iris_api)
			self.driver.save_screenshot(sel.get_screenshot_filename())
			self.driver.quit()
			self.server.stop()
			raise

	def tearDown(self):
	# close the browser window
		self.driver.quit()
		self.server.stop()
		if headless:
			self.display.stop()

if __name__ == '__main__':
    unittest.main(verbosity=2)