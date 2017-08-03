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
class TestPlatformId(object):
	def test_platform_id_passed(self,selenium,proxy):
		#Test to check for platform_id passed by Javascript for update calls was contained in the paylist returned by API
		#NOTE: once the last asset is reached it will not play any more videos since it does not play duplicates
		try:
			driver=selenium
			time.sleep(3)
			player = Player(driver,timeout,preroll_ads)
			player.wait_for_forward()
			filter = Harfilter(proxy.har)
			iris_files = filter._filter_return_iris_files(sel.iris_path)
			httpErrors = filter._filter_check_all_errors(sel.iris_path)
			assert len(httpErrors) == 0, "Some files failed to load due to HTTP errors"
			if '.js' not in sel.check_iris_files(iris_files):
				print "Iris JS file missing\n"
			player.wait_for_ad()
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
			playlist = sel.get_playlist(watch_list)
			platform_id_list = sel.get_platform_ids(watch_list)
			y=len(jsonObj["next"])
			print "\nTotal initial asset list: " + str(y)
			if y in range(1,4):
				print "WARN: Watch call has less than 4 assets"
			for x in range(y-1):
				player.click_forward()
				time.sleep(3)
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
			sel.total_calls(watch_calls,update_calls,next_calls)
			apiErrors = filter._filter_check_all_errors(sel.iris_api)
			for x in range(0,len(update_qstrings)):
				temp_plat = update_qstrings[x].get("platform_id","")
				assert temp_plat in platform_id_list, "platform_id: " + str(temp_plat) + ", was not in watch playlist returned by API"
			platform_id_update = sel.check_platform_id(update_qstrings)
			platform_id_next = sel.check_platform_id(next_qstrings)
			if platform_id_update> 0 or platform_id_next> 0:
				watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
				if len(watch_list) > 0:
					jsonObj = sel.get_json(watch_list)
					print "\nWatch call response: \n" + str(json.dumps(sel.get_json(watch_list), ensure_ascii=True))
			assert platform_id_update== 0, "There was " + str(platform_id_update) + " update calls missing platform_id"
			assert platform_id_next== 0, "There was " + str(platform_id_next) + " next calls missing platform_id"
			assert watch_success == True, "success did not equal true in watch call response"
			next_list = filter._filter_entries_by_url_response(sel.iris_next)
			if len(next_list) > 0:
				next_success_total = sel.check_response(next_list)
				assert next_success_total == 0, "Some next calls did not contain \"success\":true, " + next_success_total + " calls"
				assert sel.check_for_dup_recs(playlist,next_list) == False, "Next call contained duplicate recs from initial watch call"
			next_count = sel.count_actions(update_qstrings,"behavior[next]")
			print "\nTotal update calls with behavior[next]: " + str(next_count)
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