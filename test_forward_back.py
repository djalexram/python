import pytest
from filter import Harfilter
from sel import Player
from selenium import webdriver


import ast
import json
import time
import sel

@pytest.mark.regression
@pytest.mark.accounts
@pytest.mark.nothumbs
class TestForwardBack(object):
	def test_forward_back(self,selenium,proxy,preroll_ads,accounts,player_num,env,log,check_player_url,api_test):
		api_path = iris_api
		watch_list = []
		iris_config = dict()
		try:
			driver = selenium
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
			og_plat = player.get_current_platformID()
			next_plat = player.get_playlist_platformID(1)
			player.click_forward()
			player.wait_for_ad()
			if not accounts and next_plat:
				print "Expected platformID: " + next_plat
				assert next_plat == player.get_current_platformID(), "Expected platform id does not match with current"
				filter = Harfilter(proxy.har)
				update_calls =  filter._filter_return_request_querystring(sel.iris_update)
				assert sel.check_behavior(update_calls,"behavior[next]") == "1", "behavior[next]=1 not found in recent requests"
			#assert sel.check_behavior(update_calls,"behavior[play]") == "1", "behavior[play]=1 not found in recent requests"
				preIndex = int(player.get_currentIndex()) -1
			player.click_back()
			player.wait_for_ad()
			if not accounts and next_plat:
				assert player.get_playlist_platformID(preIndex) == player.get_current_platformID(), "Expected platform id does not match with current"
			url = driver.current_url
			time.sleep(2)
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
			if "https:" in url:
				dom_files = player.get_iris_files()
				if dom_files:
					assert "api.iris" in dom_files and "http://api.iris" not in dom_files, "Iris API calls are being blocked, make sure client adds Iris config ssl=true OR load as HTTP: instead"
				watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
				if len(watch_list) >=1:
					asset_url_list = sel.get_asset_urls(watch_list)
					if asset_url_list and "http:" in ','.join(asset_url_list):
						print error_messages['update feed rec']
					image_asset_list = sel.get_asset_images(watch_list)
					if image_asset_list and "http:" in ','.join(image_asset_list):
						print error_messages['update feed image']
			assert platform_id_update== 0, "There was " + str(platform_id_update) + " update calls missing platform_id"
			assert platform_id_next== 0, "There was " + str(platform_id_next) + " next calls missing platform_id"
			next_list = filter._filter_entries_by_url_response(sel.iris_next)
			if len(next_list) > 0:
				next_success_total = sel.check_response(next_list)
				assert next_success_total == 0, "Some next calls did not contain \"success\":true, " + next_success_total + " calls"
			if not accounts:
				assert sel.count_actions(update_qstrings,"behavior[next]") in range(2,4)
				assert len(watch_calls) == expected_watch, "Extra watch calls: " + str(len(watch_calls)-1)
			update_min = 3
			maxi = 11
			maxi = sel.update_maxi(maxi)
			#if not accounts:
			#	assert len(update_calls) in range(update_min,maxi), "Expected total update calls in range " + str(update_min) + "-" + str(maxi-1) + ", found: " + str(len(update_calls))
			#assert len(apiErrors) == 0, "Some API calls failed due to HTTP errors"

		except AssertionError:
			raise

		except:
			driver.save_screenshot(sel.get_screenshot_filename(path))
			raise

		finally:
			if log:
				sel.get_plugin_ver(log)
			filter = Harfilter(proxy.har)
			watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
			api_qstrings = filter._filter_return_request_querystring(api_path)
			if len(api_qstrings) >0:
				userid_status = sel.get_api_calls(api_qstrings,iris_config.get("user_id"))
				response_list = filter._filter_entries_by_response(iris_watch_next)
				sel.print_responses(response_list)
				bcov_list = filter._filter_return_url(bcov_player)
				if bcov_list:
					print "\nBrightcove player(s):"
					for b in bcov_list:
						print str(b)
				if not accounts:
					assert userid_status, "Appears user_id was not same for all api calls"
			apiErrors = filter._filter_return_errors(api_path)
			if api_test:
				assert len(apiErrors) == 0, error_messages['api error']
			cookies = driver.get_cookies()
			if cookies:
				cookie = player.get_iris_cookie(cookies)
				if not accounts and not check_player_url:
					if iris_config and iris_config.get('set_cookie') == True:
						assert cookie, "userid cookie was not created"
					elif iris_config.get('set_cookie') is None:
						print "set_cookie: None" 
					else:
						assert not cookie, "userid cookie should not have been created"
			iris_files = filter._filter_return_url_from_list(iris_scripts)
			httpErrors = filter._filter_return_errors(iris_prod)
			watch_json = sel.get_json(watch_list)
			vast_tag = sel.get_vast_tag(watch_json)
			if len(iris_files) >0:
				print "\nIRIS FILES:"
				for x in iris_files:
					print x
			if len(iris_files) >0 and '.js' not in sel.check_iris_files(iris_files):
				print "Iris JS file missing\n"
			bcovErrors = filter._filter_return_errors(bcov_cms)
			if len(bcovErrors) >0:
				print error_messages['bcov cms']
				print error_messages['video not found'] + str(sel.get_cms_ids(bcovErrors))
			jwErrors = filter._filter_return_errors(jw_feed)
			if len(jwErrors) >0:
				print error_messages['jw feed']
			if check_player_url and len(watch_list) > 0:
				playlist = sel.get_playlist(watch_list)
				next_list = filter._filter_entries_by_url_response(iris_next)
				if check_player_url and len(next_list) > 0:
					dup_recs = sel.check_for_dup_recs(playlist,next_list)
					if dup_recs and len(dup_recs) > 1:
						print error_messages['dup recs'] + ", platform id(s): " + str(dup_recs)
				assert sel.check_for_dup_asset(playlist) == False, error_messages['dup asset']