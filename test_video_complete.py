import pytest  
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

@pytest.mark.regression
class TestVideoComplete(object):

	def test_video_complete(self,selenium,proxy,skip_forward_present,preroll_ads,accounts,player_num,env,log,check_player_url,api_test):
		api_path = iris_api
		videos_played =[]
		iris_config = dict()
		try:
			driver=selenium
			player = Player(driver,timeout,preroll_ads,player_num)
			player.wait_for_ad()
			if skip_forward_present:
				player.wait_for_forward()
			print "Waiting for video to finish playing and autoplay next asset"
			player.get_first_video()
			player.check_if_paused()
			filter = Harfilter(proxy.har)
			watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
			if len(watch_list) == 0:
				for x in range (1,7):
					print "waiting for first watch call"
					time.sleep(5)
					filter = Harfilter(proxy.har)
					watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
					if len(watch_list) > 0:
						break
			url = driver.current_url
			secure = False
			if "https:" in url:
				secure = True
				dom_files = player.get_iris_files()
				if dom_files:
					assert "api.iris" in dom_files and "http://api.iris" not in dom_files, "Iris API calls are being blocked, make sure client adds Iris config ssl=true OR load as HTTP: instead"
				if len(watch_list) >=1:
					asset_url_list = sel.get_asset_urls(watch_list)
					if asset_url_list and "http:" in ','.join(asset_url_list):
						print error_messages['update feed rec']
					image_asset_list = sel.get_asset_images(watch_list)
					if image_asset_list and "http:" in ','.join(image_asset_list):
						print error_messages['update feed image']
			assert len(watch_list) != 0, "No watch calls found"
			playlist = sel.get_playlist(watch_list)
			watch_qstrings = filter._filter_return_request_querystring(sel.iris_watch)
			iris_config = sel.set_watch_call_params(watch_qstrings)
			if secure and not iris_config["ssl"]:
				print "Make sure client adds Iris config ssl=true OR load as HTTP: instead"
			jsonObj = sel.get_json(watch_list)
			watch_success = sel.check_single_response(watch_list)
			playlist_len = sel.get_playlist_length(watch_list)
			print "\nTotal initial asset list: " + str(playlist_len)
			if playlist_len < 2:
				print "WARNING: Looks like no recs are being returned"
			elif playlist_len in range(1,4):
				print "WARNING: Watch call has less than 4 assets"
			watch_json = sel.get_json(watch_list)
			sel.get_vast_tag(watch_json)
			print "\nWatch call response: \n" + str(json.dumps(watch_json, ensure_ascii=True)) + "\n"
			temp = player.get_first_video()
			if temp:
				videos_played.append(temp)
			if accounts:
				player.scrub()
			element = WebDriverWait(driver, max_timeout).until(
				wait_for_video_to_change(player_num)
			)
			temp2 = player.get_first_video()
			if temp2:
				videos_played.append(temp2)
			time.sleep(2)
			filter = Harfilter(proxy.har)
			watch_calls =  filter.get_matches(sel.iris_watch)
			update_calls =  filter.get_matches(sel.iris_update)
			next_calls =  filter.get_matches(sel.iris_next)
			watch_qstrings = filter._filter_return_request_querystring(sel.iris_watch)
			update_qstrings = filter._filter_return_request_querystring(sel.iris_update)
			next_qstrings = filter._filter_return_request_querystring(sel.iris_next)
			api_qstrings = filter._filter_return_request_querystring(iris_api)
			sel.set_watch_call_params(watch_qstrings)
			platform_id_update = sel.check_platform_id(update_qstrings)
			platform_id_next = sel.check_platform_id(next_qstrings)
			assert platform_id_update== 0, "There was " + str(platform_id_update) + " update calls missing platform_id"
			assert platform_id_next== 0, "There was " + str(platform_id_next) + " next calls missing platform_id"
			assert watch_success == True, "success did not equal true in watch call response"
			percent_watched = sel.get_percentage_watched(update_qstrings)
			seconds_watched = sel.get_seconds_watched(update_qstrings)
			print "\nCampaign tracking beacons: " + str(percent_watched)
			print "\nSeconds beacons: " + str(seconds_watched)
			sel.total_calls(watch_calls,update_calls,next_calls)
			assert sel.check_behavior(update_qstrings,"behavior[video_complete]") == "1", "Could not find request with behavior[video_complete]"
			if not accounts:
				assert len(watch_calls) == expected_watch, "Extra watch calls: " + str(len(watch_calls)-1)
				if sel.campaign_tracking == False:
					assert len(percent_watched) == 1, "Expected 1 campaign tracking beacon, found: " + str(len(percent_watched))
					assert len(seconds_watched) == 0, "Expected 0 seconds beacons, found: " + str(len(seconds_watched))
				elif sel.campaign_tracking == True:
					assert len(percent_watched) == 3, "Expected 3 campaign tracking beacons, found: " + str(len(percent_watched))
					assert len(seconds_watched) >= 5, "Expected 5 seconds beacons, found: " + str(len(seconds_watched))
			maxi = 11
			update_min = 2
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
			watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
			if len(watch_list) > 0:
				watch_json = sel.get_json(watch_list)
				sel.get_vast_tag(watch_json)
			if len(videos_played) > 0 and len(videos_played) != 2:
				print error_messages['playback'] + " first asset from watch call did not play"
			jwErrors = filter._filter_return_errors(jw_feed)
			if len(jwErrors) >0:
				print error_messages['jw feed']
			bcovErrors = filter._filter_return_errors(bcov_cms)
			if len(bcovErrors) >0:
				print error_messages['bcov cms']
				print error_messages['video not found'] + str(sel.get_cms_ids(bcovErrors))
			if check_player_url and len(watch_list) > 0:
				playlist = sel.get_playlist(watch_list)
				next_list = filter._filter_entries_by_url_response(iris_next)
				if check_player_url and len(next_list) > 0:
					dup_recs = sel.check_for_dup_recs(playlist,next_list)
					if dup_recs and len(dup_recs) > 1:
						print error_messages['dup recs'] + ", platform id(s): " + str(dup_recs)
				assert sel.check_for_dup_asset(playlist) == False, error_messages['dup asset']
