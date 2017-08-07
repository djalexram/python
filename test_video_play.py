import pytest
from browsermobproxy import Server   
from filter import Harfilter
from sel import Player,wait_for_video_to_change, wait_for_first_video,wait_for_page_load
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locators import PlayerLocators
from selenium import webdriver

import ast
import json
import time
import sel
import sys

@pytest.mark.nobuttons
class TestVideoPlay(object):

	def test_video_play(self,selenium,proxy,server):
		try:
			driver=selenium
			if player_type == "vdb":
				print "waiting for player bar to load"
				element = WebDriverWait(self.driver, timeout).until(
					EC.presence_of_element_located((PlayerLocators.VDB_PLAYER_BAR))
					)
			player = Player(driver,timeout,preroll_ads)
			if skip_forward_present:
				player.wait_for_forward()
			player.wait_for_ad()
			url = driver.current_url
			if ".nfl." in url:
				checkbox_list = driver.find_elements(*PlayerLocators.NFL_ENABLE_IRIS)
				if len(checkbox_list) > 0:
					checkbox_list[0].click()
					print "click checkbox"
			filter = Harfilter(proxy.har)
			watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
			if len(watch_list) == 0:
				print "waiting for first watch call"
				time.sleep(10)
				filter = Harfilter(proxy.new_har)
				watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
				if len(watch_list) == 0:
					print "waiting for first watch call"
					time.sleep(15)
					filter = Harfilter(proxy.har)
					watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
			if len(watch_list) >=1:
				watch_success = sel.check_single_response(watch_list)
				print "\nWatch call response: \n" + str(json.dumps(sel.get_json(watch_list), ensure_ascii=True))
				rec_len = sel.get_playlist_length(watch_list)
				print "\nTotal initial asset list: " + str(rec_len)
				if rec_len in range(1,4):
					print "WARN: Watch call has less than 4 assets"
			if not player.get_first_video():
				element = WebDriverWait(driver, timeout).until(
					wait_for_first_video()
					)
			#player.click_end_next_slate()
			filter = Harfilter(proxy.har)
			iris_files = filter._filter_return_iris_files(sel.iris_path)
			httpErrors = filter._filter_check_all_errors(sel.iris_path)
			assert len(httpErrors) == 0, "Some files failed to load due to HTTP errors"
			if '.js' not in sel.check_iris_files(iris_files):
				print "Iris JS file missing\n"
			print "\nWaiting for video to finish playing and autoplay next asset"
			for x in range(1,4):
				player.get_first_video()
				element = WebDriverWait(driver, max_timeout).until(
					wait_for_video_to_change()
					)
				time.sleep(2)
			filter = Harfilter(proxy.har)
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
			assert len(watch_calls) == expected_watch, "Extra watch calls: " + str(len(watch_calls)-1)
			assert len(apiErrors) == 0, "Some API calls failed due to HTTP errors"
			

		except AssertionError:
			raise

		except:
			filter = Harfilter(proxy.har)
			watch_calls =  filter.get_matches(sel.iris_watch)
			update_calls =  filter.get_matches(sel.iris_update)
			next_calls =  filter.get_matches(sel.iris_next)
			watch_qstrings = filter._filter_return_request_querystring(sel.iris_watch)
			update_qstrings = filter._filter_return_request_querystring(sel.iris_update)
			next_qstrings = filter._filter_return_request_querystring(sel.iris_next)
			if len(watch_qstrings) >0:
				sel.get_watch_calls(watch_qstrings)
				sel.get_update_calls(update_qstrings)
				sel.get_next_calls(next_qstrings)
			apiErrors = filter._filter_check_all_errors(sel.iris_api)
			driver.save_screenshot(sel.get_screenshot_filename())
			driver.quit()
			raise