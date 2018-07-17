import pytest
from filter import Harfilter
from sel import Player
from selenium import webdriver

import ast
import json
import time
import sel

@pytest.mark.regression
class TestUpNextSlates(object):

	def test_start_next_slate(self,selenium,proxy,preroll_ads,skip_forward_present,accounts,player_num,env,log,check_player_url,api_test):
		api_path = iris_api
		iris_config = dict()
		try:
			driver=selenium
			url = driver.current_url
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
						time.sleep(2)
						filter = Harfilter(proxy.har)
						watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
						if len(watch_list) > 0:
							break
			next_plat = player.get_playlist_platformID(2)
			player.click_forward()
			player.wait_for_ad()
			player.check_if_paused()
			if not accounts and next_plat:
				index = int(player.get_currentIndex()) +1
			print "Waiting for start next slate to appear"
			text = player.get_start_next_slate()
			print "Start next slate text: " + text
			player.wait_for_ad()
			if not accounts and next_plat:
				print "Expected platformID: " + next_plat
				assert player.get_playlist_platformID(index) == player.get_current_platformID(), "Expected platform id does not match with current"
			time.sleep(4)
			filter = Harfilter(proxy.har)
			watch_qstrings = filter._filter_return_request_querystring(sel.iris_watch)
			update_qstrings = filter._filter_return_request_querystring(sel.iris_update)
			next_qstrings = filter._filter_return_request_querystring(sel.iris_next)
			api_qstrings = filter._filter_return_request_querystring(iris_api)
			iris_config = sel.set_watch_call_params(watch_qstrings)
			#assert sel.check_behavior(update_qstrings,"behavior[play]") == "1", "behavior[play]=1, not found in requests"

			watch_calls =  filter.get_matches(sel.iris_watch)
			update_calls =  filter.get_matches(sel.iris_update)
			next_calls =  filter.get_matches(sel.iris_next)
			sel.total_calls(watch_calls,update_calls,next_calls)
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
			#assert sel.count_actions(update_qstrings,"behavior[next]") == 1, "Expected only 1 request with behavior[next], found: " + str(sel.count_actions(update_qstrings,"behavior[next]"))
			assert sel.count_actions(update_qstrings,"behavior[start_next_slate]") == 1,"Expected only 1 request with behavior[start_next_slate], found: " + str(sel.count_actions(update_qstrings,"behavior[end_next_slate]"))
			next_list = filter._filter_entries_by_url_response(sel.iris_next)
			if len(next_list) > 0:
				next_success_total = sel.check_response(next_list)
				assert next_success_total == 0, "Some next calls did not contain \"success\":true, " + next_success_total + " calls"
				if check_player_url:
					assert sel.check_for_dup_recs(playlist,next_list) == False, "Next call contained duplicate recs from initial watch call"
			assert sel.count_actions(update_qstrings,"behavior[play]") in range(1,4)
			if not accounts:
				assert len(watch_calls) == expected_watch, "Extra watch calls: " + str(len(watch_calls)-1)
			update_min = 3
			maxi = 7
			maxi = sel.update_maxi(maxi)
			#if not accounts:
			#	assert len(update_calls) in range(update_min,maxi), "Expected total update calls in range " + str(update_min) + "-" + str(maxi-1) + ", found: " + str(len(update_calls))
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

	def test_end_next_slate(self,selenium,proxy,preroll_ads,skip_forward_present,accounts,player_num,env,log,check_player_url,api_test):
		api_path = iris_api
		iris_config = dict()
		try:
			driver=selenium
			player = Player(driver,timeout,preroll_ads,player_num)
			player.wait_for_ad()
			if skip_forward_present:
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
			next_plat = player.get_playlist_platformID(1)
			print "Waiting for end next slate to appear"
			player.scrub()
			text = player.get_end_next_slate(max_timeout)
			print "End next slate text: " + text
			player.wait_for_ad()
			if not accounts and next_plat:
				print "Expected platformID: " + next_plat
				assert next_plat == player.get_current_platformID(), "Expected platform id does not match with current"
			time.sleep(4)
			filter = Harfilter(proxy.har)
			watch_qstrings = filter._filter_return_request_querystring(sel.iris_watch)
			update_qstrings = filter._filter_return_request_querystring(sel.iris_update)
			next_qstrings = filter._filter_return_request_querystring(sel.iris_next)
			api_qstrings = filter._filter_return_request_querystring(iris_api)
			iris_config = sel.set_watch_call_params(watch_qstrings)
			assert sel.check_behavior(update_qstrings,"behavior[next]") == "1", "behavior[next]=1, not found in requests"
			#assert sel.check_behavior(update_qstrings,"behavior[play]") == "1", "behavior[play]=1, not found in requests"

			watch_calls =  filter.get_matches(sel.iris_watch)
			update_calls =  filter.get_matches(sel.iris_update)
			next_calls =  filter.get_matches(sel.iris_next)
			sel.total_calls(watch_calls,update_calls,next_calls)
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
					print "\nWatch call response: \n" + str(json.dumps(sel.get_json(watch_list), ensure_ascii=True))
			assert platform_id_update== 0, "There was " + str(platform_id_update) + " update calls missing platform_id"
			assert platform_id_next== 0, "There was " + str(platform_id_next) + " next calls missing platform_id"
			assert sel.count_actions(update_qstrings,"behavior[next]") == 1, "Expected only 1 request with behavior[next], found: " + str(sel.count_actions(update_qstrings,"behavior[next]"))
			assert sel.count_actions(update_qstrings,"behavior[end_next_slate]") == 1,"Expected only 1 request with behavior[end_next_slate], found: " + str(sel.count_actions(update_qstrings,"behavior[end_next_slate]"))
			next_list = filter._filter_entries_by_url_response(sel.iris_next)
			if len(next_list) > 0:
				next_success_total = sel.check_response(next_list)
				assert next_success_total == 0, "Some next calls did not contain \"success\":true, " + next_success_total + " calls"
				if check_player_url:
					assert sel.check_for_dup_recs(playlist,next_list) == False, "Next call contained duplicate recs from initial watch call"
			#assert sel.count_actions(update_qstrings,"behavior[play]") in [1,2]
			if not accounts:
				assert len(watch_calls) == expected_watch, "Extra watch calls: " + str(len(watch_calls)-1)
			update_min = 3
			maxi = 7
			maxi = sel.update_maxi(maxi)
			#if not accounts:
			#	assert len(update_calls) in range(update_min,maxi), "Expected total update calls in range " + str(update_min) + "-" + str(maxi-1) + ", found: " + str(len(update_calls))
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
				response_list = filter._filter_entries_by_response(iris_watch_next)
				sel.print_responses(response_list)
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