import pytest
from filter import Harfilter
from sel import Player
from selenium import webdriver

import ast
import json
import time
import sel

@pytest.mark.regression
class TestPlatformId(object):
	def test_platform_id_passed(self,selenium,proxy,preroll_ads,accounts,player_num,env,log,check_player_url,api_test):
		#Test to check for platform_id passed by Javascript for update calls was contained in the paylist returned by API
		#NOTE: once the last asset is reached it will not play any more videos since it does not play duplicates
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
			assert len(watch_list) > 0, "No watch call found"
			jsonObj = sel.get_json(watch_list)
			watch_success = sel.check_single_response(watch_list)
			playlist = sel.get_playlist(watch_list)
			platform_id_list = sel.get_platform_ids(watch_list)
			y=len(jsonObj["next"])
			print "\nTotal initial asset list: " + str(y)
			if y in range(1,4):
				print "WARNING: Watch call has less than 4 assets"
			for x in range(y-1):
				player.wait_for_ad()
				player.click_forward()
			filter = Harfilter(proxy.har)
			watch_calls =  filter.get_matches(sel.iris_watch)
			update_calls =  filter.get_matches(sel.iris_update)
			next_calls =  filter.get_matches(sel.iris_next)
			watch_qstrings = filter._filter_return_request_querystring(sel.iris_watch)
			update_qstrings = filter._filter_return_request_querystring(sel.iris_update)
			next_qstrings = filter._filter_return_request_querystring(sel.iris_next)
			api_qstrings = filter._filter_return_request_querystring(iris_api)
			iris_config = sel.set_watch_call_params(watch_qstrings)
			sel.total_calls(watch_calls,update_calls,next_calls)
			# for x in range(0,len(update_qstrings)-1):
			# 	temp_plat = update_qstrings[x].get("platform_id","")
			# 	assert temp_plat in platform_id_list, "platform_id: " + str(temp_plat) + ", was not in watch playlist returned by API"
			platform_id_update = sel.check_platform_id(update_qstrings)
			platform_id_next = sel.check_platform_id(next_qstrings)
			if platform_id_update> 0 or platform_id_next> 0:
				watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
				if len(watch_list) > 0:
					jsonObj = sel.get_json(watch_list)
					print "\nWatch call response: \n" + str(json.dumps(sel.get_json(watch_list), ensure_ascii=True)) + "\n"
			assert platform_id_update== 0, "There was " + str(platform_id_update) + " update calls missing platform_id"
			assert platform_id_next== 0, "There was " + str(platform_id_next) + " next calls missing platform_id"
			assert watch_success == True, "success did not equal true in watch call response"
			next_list = filter._filter_entries_by_url_response(sel.iris_next)
			if len(next_list) > 0:
				next_success_total = sel.check_response(next_list)
				assert next_success_total == 0, "Some next calls did not contain \"success\":true, " + next_success_total + " calls"
			next_count = sel.count_actions(update_qstrings,"behavior[next]")
			print "\nTotal update calls with behavior[next]: " + str(next_count)
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