import pytest
from browsermobproxy import Server   
from filter import Harfilter
from sel import Player,wait_for_index_to_change, wait_for_video_to_change
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver

import ast
import json
import time
import sel


class TestVideoComplete(object):

	def test_video_complete(self,selenium,proxy):
		try:
			driver=selenium
			player = Player(driver,timeout)
			player.wait_for_forward()
			time.sleep(3)
			filter = Harfilter(proxy.har)
			iris_files = filter._filter_return_iris_files(sel.iris_path)
			httpErrors = filter._filter_check_all_errors(sel.iris_path)
			assert len(httpErrors) == 0, "Some files failed to load due to HTTP errors"
			if '.js' not in sel.check_iris_files(iris_files):
				print "Iris JS file missing\n"
			print "Waiting for video to finish playing and autoplay next asset"
			player.wait_for_ad()
			player.get_first_video()
			filter = Harfilter(proxy.har)
			watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
			if len(watch_list) == 0:
				print "waiting for first watch call"
				time.sleep(10)
				filter = Harfilter(proxy.har)
				watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
				if len(watch_list) == 0:
					print "waiting for first watch call"
					time.sleep(15)
					filter = Harfilter(proxy.har)
					watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
			jsonObj = sel.get_json(watch_list)
			watch_success = sel.check_single_response(watch_list)
			playlist_len = sel.get_playlist_length(watch_list)
			print "\nTotal initial asset list: " + str(playlist_len)
			if playlist_len in range(1,4):
				print "WARN: Watch call has less than 4 assets"
			print "\nWatch call response: \n" + str(json.dumps(sel.get_json(watch_list), ensure_ascii=True))
			element = WebDriverWait(driver, max_timeout).until(
				wait_for_video_to_change()
			)
			time.sleep(2)
			filter = Harfilter(proxy.har)
			watch_calls =  filter.get_matches(sel.iris_watch)
			update_calls =  filter.get_matches(sel.iris_update)
			next_calls =  filter.get_matches(sel.iris_next)
			watch_qstrings = filter._filter_return_request_querystring(sel.iris_watch)
			update_qstrings = filter._filter_return_request_querystring(sel.iris_update)
			next_qstrings = filter._filter_return_request_querystring(sel.iris_next)
			sel.get_watch_calls(watch_qstrings)
			sel.get_update_calls(update_qstrings)
			sel.get_next_calls(next_qstrings)
			platform_id_update = sel.check_platform_id(update_qstrings)
			platform_id_next = sel.check_platform_id(next_qstrings)
			apiErrors = filter._filter_check_all_errors(sel.iris_api)
			assert platform_id_update== 0, "There was " + str(platform_id_update) + " update calls missing platform_id"
			assert platform_id_next== 0, "There was " + str(platform_id_next) + " next calls missing platform_id"
			assert watch_success == True, "success did not equal true in watch call response"
			percent_watched = sel.get_percentage_watched(update_qstrings)
			print "\nCampaign tracking beacons: " + str(percent_watched)
			if sel.campaign_tracking == False:
				assert len(percent_watched) == 1, "Expected 1 campaign tracking beacon, found: " + str(len(percent_watched))
			elif sel.campaign_tracking == True:
				assert len(percent_watched) == 3, "Expected 3 campaign tracking beacons, found: " + str(len(percent_watched))
			sel.total_calls(watch_calls,update_calls,next_calls)
			assert sel.check_behavior(update_qstrings,"behavior[video_complete]") == "1", "Could not find request with behavior[video_complete]"
			assert len(watch_calls) == expected_watch, "Extra watch calls: " + str(len(watch_calls)-1)
			maxi = 6
			update_min = 2
			maxi = sel.update_maxi(maxi)
			assert len(update_calls) in range(update_min,maxi), "Expected total update calls in range " + str(update_min) + "-" + str(maxi-1) + ", found: " + str(len(update_calls))
			assert len(apiErrors) == 0, "Some API calls failed due to HTTP errors"

	
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