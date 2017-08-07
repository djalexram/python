import pytest
from browsermobproxy import Server
from filter import Harfilter
from sel import Player
from selenium import webdriver


import ast
import json
import time
import sel

@pytest.mark.regression
@pytest.mark.nothumbs
class TestForwardBack(object):
	def test_forward_back(self,selenium,proxy,server):
		try:
			driver = selenium
			player = Player(driver,timeout,preroll_ads)
			player.wait_for_forward()
			time.sleep(3)
			filter = Harfilter(proxy.new_har)
			iris_files = filter._filter_return_iris_files(sel.iris_path)
			httpErrors = filter._filter_check_all_errors(sel.iris_path)
			assert len(httpErrors) == 0, "Some Iris files failed to load due to HTTP errors"
			if '.js' not in sel.check_iris_files(iris_files):
				print "Iris JS file missing\n"
			player.wait_for_ad()
			player.click_forward()
			time.sleep(5)
			player.wait_for_ad()
			filter = Harfilter(proxy.har)
			update_calls =  filter._filter_return_request_querystring(sel.iris_update)
			assert sel.check_behavior(update_calls,"behavior[next]") == "1", "behavior[next]=1 not found in recent requests"
			#assert sel.check_behavior(update_calls,"behavior[play]") == "1", "behavior[play]=1 not found in recent requests"
			player.click_back()
			time.sleep(2)
			filter = Harfilter(proxy.har)
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
			watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
			if len(watch_list) > 0:
				jsonObj = sel.get_json(watch_list)
				playlist = sel.get_playlist(watch_list)
				watch_success = sel.check_single_response(watch_list)
				rec_len = sel.get_playlist_length(watch_list)
				print "\nTotal initial asset list: " + str(rec_len)
				if rec_len in range(1,4):
					print "WARN: Watch call has less than 4 assets"
				if platform_id_update> 0 or platform_id_next> 0:
					print "\nWatch call response: \n" + str(json.dumps(sel.get_json(watch_list), ensure_ascii=True))
			apiErrors = filter._filter_check_all_errors(sel.iris_api)
			assert platform_id_update== 0, "There was " + str(platform_id_update) + " update calls missing platform_id"
			assert platform_id_next== 0, "There was " + str(platform_id_next) + " next calls missing platform_id"
			next_list = filter._filter_entries_by_url_response(sel.iris_next)
			if len(next_list) > 0:
				next_success_total = sel.check_response(next_list)
				assert next_success_total == 0, "Some next calls did not contain \"success\":true, " + next_success_total + " calls"
				assert sel.check_for_dup_recs(playlist,next_list) == False, "Next call contained duplicate recs from initial watch call"
			lastUpdate=update_qstrings[len(update_qstrings)-1]
			assert sel.count_actions(update_qstrings,"behavior[next]") == 2
			assert len(watch_calls) == expected_watch, "Extra watch calls: " + str(len(watch_calls)-1)
			update_min = 3
			maxi = 9
			maxi = sel.update_maxi(maxi)
			assert len(update_calls) in range(update_min,maxi), "Expected total update calls in range " + str(update_min) + "-" + str(maxi-1) + ", found: " + str(len(update_calls))
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
			#proxy.close()
			#server.stop()
			raise