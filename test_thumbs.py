
import pytest  
from filter import Harfilter
from sel import Player,wait_for_video_to_change
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver

import ast
import json
import time
import sel

@pytest.mark.regression
class TestThumbs(object):
	def test_thumb_down(self,selenium,proxy,preroll_ads,accounts,player_num,env,log,check_player_url,api_test):
		api_path = iris_api
		iris_config = dict()
		try:
			driver=selenium
			player = Player(driver,timeout,preroll_ads,player_num)
			player.wait_for_ad()
			player.wait_for_forward()
			player.check_if_paused()
			if proxy:
				filter = Harfilter(proxy.har)
				watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
				if len(watch_list) == 0:
					for x in range (1,7):
						print "waiting for first watch call"
						time.sleep(3)
						filter = Harfilter(proxy.har)
						watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
						if len(watch_list) > 0:
							break
			curr_plat = player.get_current_platformID()
			player.click_thumb_down()
			player.wait_for_ad()
			if not accounts and curr_plat:
				assert curr_plat != player.get_current_platformID(), "Expected platform id does not match with current"
			time.sleep(3)
			filter = Harfilter(proxy.har)
			watch_calls =  filter.get_matches(sel.iris_watch)
			update_calls =  filter.get_matches(sel.iris_update)
			next_calls =  filter.get_matches(sel.iris_next)
			watch_qstrings = filter._filter_return_request_querystring(sel.iris_watch)
			update_qstrings = filter._filter_return_request_querystring(sel.iris_update)
			next_qstrings = filter._filter_return_request_querystring(sel.iris_next)
			api_qstrings = filter._filter_return_request_querystring(iris_api)
			iris_config = sel.set_watch_call_params(watch_qstrings)
			platform_id_update = sel.check_platform_id(update_qstrings)
			platform_id_next = sel.check_platform_id(next_qstrings)
			watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
			if len(watch_list) > 0:
				jsonObj = sel.get_json(watch_list)
				playlist = sel.get_playlist(watch_list)
				watch_success = sel.check_single_response(watch_list)
				rec_len = sel.get_playlist_length(watch_list)
				print "\nTotal initial asset list: " + str(rec_len)
				if rec_len < 2:
					print "WARNING: Looks like no recs are being returned"
				elif rec_len in range(1,4):
					print "WARNING: Watch call has less than 4 assets"
				if platform_id_update> 0 or platform_id_next> 0:
					print "\nWatch call response: \n" + str(json.dumps(sel.get_json(watch_list), ensure_ascii=True)) + "\n"
			assert platform_id_update== 0, "There was " + str(platform_id_update) + " update calls missing platform_id"
			assert platform_id_next== 0, "There was " + str(platform_id_next) + " next calls missing platform_id"
			next_list = filter._filter_entries_by_url_response(sel.iris_next)
			if len(next_list) > 0:
				next_success_total = sel.check_response(next_list)
				assert next_success_total == 0, "Some next calls did not contain \"success\":true, " + next_success_total + " calls"
				if check_player_url:
					assert sel.check_for_dup_recs(playlist,next_list) == False, "Next call contained duplicate recs from initial watch call"
			assert sel.check_behavior(update_qstrings,"behavior[thumbs_down]") == "1", "behavior[thumbs_down] = 1 not found in requests"
			assert len(watch_calls) == expected_watch, "Extra watch calls: " + str(len(watch_calls)-1)
			update_min = 3
			maxi = 10
			maxi = sel.update_maxi(maxi)
			if not accounts:
				#assert len(update_calls) in range (update_min,maxi), "Expected total update calls in range " + str(update_min) + "-" + str(maxi-1) + ", found: " + str(len(update_calls))
				assert len(next_calls) in range(1,3), "Failed due to extra next calls"
			sel.total_calls(watch_calls,update_calls,next_calls)
			#assert len(apiErrors) == 0, "Some API calls failed due to HTTP errors"

		except AssertionError:
			raise

		except:
			driver.save_screenshot(sel.get_screenshot_filename(path))
			driver.quit()
			raise

		finally:
			if log:
				sel.get_plugin_ver(log)
			filter = Harfilter(proxy.har)
			api_qstrings = filter._filter_return_request_querystring(api_path)
			if len(api_qstrings) >0:
				sel.get_api_calls(api_qstrings)
			apiErrors = filter._filter_return_errors(api_path)
			if api_test:
				assert len(apiErrors) == 0, error_messages['api error']
			iris_files = filter._filter_return_url_from_list(iris_scripts)
			httpErrors = filter._filter_return_errors(iris_prod)
			if len(iris_files) >0:
				print "\nIRIS FILES:"
				for x in iris_files:
					print x
			if len(iris_files) >0 and '.js' not in sel.check_iris_files(iris_files):
				print "Iris JS file missing\n"
			jwErrors = filter._filter_return_errors(jw_feed)
			if len(jwErrors) >0:
				print error_messages['jw feed']
			bcovErrors = filter._filter_return_errors(bcov_cms)
			if len(bcovErrors) >0:
				print error_messages['bcov cms']
				print error_messages['video not found'] + str(sel.get_cms_ids(bcovErrors))
	
	def test_thumb_up(self,selenium,proxy,preroll_ads,accounts,player_num,env,log,check_player_url,api_test):
		api_path = iris_api
		iris_config = dict()
		try:
			driver=selenium
			player = Player(driver,timeout,preroll_ads,player_num)
			player.wait_for_ad()
			player.wait_for_forward()
			player.check_if_paused()
			if proxy:
				filter = Harfilter(proxy.har)
				watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
				if len(watch_list) == 0:
					for x in range (1,7):
						print "waiting for first watch call"
						time.sleep(3)
						filter = Harfilter(proxy.har)
						watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
						if len(watch_list) > 0:
							break
			curr_plat = player.get_current_platformID()
			player.click_thumb_up()
			time.sleep(3)
			if not accounts and curr_plat:
				assert curr_plat == player.get_current_platformID(), "Expected platform id does not match with current"
			filter = Harfilter(proxy.har)
			watch_calls =  filter.get_matches(sel.iris_watch)
			update_calls =  filter.get_matches(sel.iris_update)
			next_calls =  filter.get_matches(sel.iris_next)
			watch_qstrings = filter._filter_return_request_querystring(sel.iris_watch)
			update_qstrings = filter._filter_return_request_querystring(sel.iris_update)
			next_qstrings = filter._filter_return_request_querystring(sel.iris_next)
			api_qstrings = filter._filter_return_request_querystring(iris_api)
			iris_config = sel.set_watch_call_params(watch_qstrings)
			platform_id_update = sel.check_platform_id(update_qstrings)
			platform_id_next = sel.check_platform_id(next_qstrings)
			watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
			if len(watch_list) > 0:
				jsonObj = sel.get_json(watch_list)
				playlist = sel.get_playlist(watch_list)
				watch_success = sel.check_single_response(watch_list)
				rec_len = sel.get_playlist_length(watch_list)
				print "\nTotal initial asset list: " + str(rec_len)
				if rec_len in range(1,4):
					print "WARNING: Watch call has less than 4 assets"
				if platform_id_update> 0 or platform_id_next> 0:
					print "\nWatch call response: \n" + str(json.dumps(sel.get_json(watch_list), ensure_ascii=True)) + "\n"
			assert platform_id_update== 0, "There was " + str(platform_id_update) + " update calls missing platform_id"
			assert platform_id_next== 0, "There was " + str(platform_id_next) + " next calls missing platform_id"
			next_list = filter._filter_entries_by_url_response(sel.iris_next)
			if len(next_list) > 0:
				next_success_total = sel.check_response(next_list)
				assert next_success_total == 0, "Some next calls did not contain \"success\":true, " + next_success_total + " calls"
			assert sel.check_behavior(update_qstrings,"behavior[thumbs_up]") == "1", "behavior[thumbs_up] = 1 not found in requests"
			if not accounts:
				assert len(watch_calls) == expected_watch, "Extra watch calls: " + str(len(watch_calls)-1)
			update_min = 3
			maxi = 10
			maxi = sel.update_maxi(maxi)
			if not accounts:
				#assert len(update_calls) in range(update_min,maxi), "Expected total update calls in range " + str(update_min) + "-" + str(maxi-1) + ", found: " + str(len(update_calls))
				assert len(next_calls) in range(1,3), "Failed due to extra next calls"
			sel.total_calls(watch_calls,update_calls,next_calls)
			#assert len(apiErrors) == 0, "Some API calls failed due to HTTP errors"


		except AssertionError:
			raise

		except:
			driver.save_screenshot(sel.get_screenshot_filename(path))
			driver.quit()
			raise

		finally:
			if log:
				sel.get_plugin_ver(log)
			filter = Harfilter(proxy.har)
			api_qstrings = filter._filter_return_request_querystring(api_path)
			if len(api_qstrings) >0:
				sel.get_api_calls(api_qstrings)
			apiErrors = filter._filter_return_errors(api_path)
			if api_test:
				assert len(apiErrors) == 0, error_messages['api error']
			iris_files = filter._filter_return_url_from_list(iris_scripts)
			httpErrors = filter._filter_return_errors(iris_prod)
			if len(iris_files) >0:
				print "\nIRIS FILES:"
				for x in iris_files:
					print x
			if len(iris_files) >0 and '.js' not in sel.check_iris_files(iris_files):
				print "Iris JS file missing\n"
			jwErrors = filter._filter_return_errors(jw_feed)
			if len(jwErrors) >0:
				print error_messages['jw feed']
			bcovErrors = filter._filter_return_errors(bcov_cms)
			if len(bcovErrors) >0:
				print error_messages['bcov cms']
				print error_messages['video not found'] + str(sel.get_cms_ids(bcovErrors))