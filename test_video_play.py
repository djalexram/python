import pytest   
from filter import Harfilter
from sel import Player,wait_for_video_to_change, wait_for_first_video,wait_for_page_load
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locators import PlayerLocators, playing_loc_list
from selenium import webdriver

import ast
import json
import time
import sel
import sys

@pytest.mark.nobuttons
@pytest.mark.videoplay
class TestVideoPlay(object):

	def test_video_play(self,selenium,proxy,preroll_ads,skip_forward_present,accounts,player_num,env,data,log,check_player_url,api_test):
		videos_played =[]
		rec_len = 0
		api_path = pytest.iris_api
		vast_tag = False
		driver=selenium
		url = driver.current_url
		iris_config = dict()
		try:
			# if player_type == "vdb":
			# 	print "waiting for player bar to load"
			# 	element = WebDriverWait(self.driver, timeout).until(
			# 		EC.presence_of_element_located((PlayerLocators.VDB_PLAYER_BAR))
			# 		)
			player = Player(driver,timeout,preroll_ads,player_num)
			player_error = player.check_for_error(path)
			player.wait_for_ad()
			if pytest.player_type == "uvpjs":
				player.wait_for_playing(playing_loc_list[0])
				time.sleep(4)
			assert player_error == False, "Player Error: " + player_error
			if skip_forward_present:
				player.wait_for_forward()
			player.check_if_paused()
			nfl = False
			if ".nfl." in url:
				nfl = True
				api_path = nfl_api
				checkbox_list = driver.find_elements(*PlayerLocators.NFL_ENABLE_IRIS)
				if len(checkbox_list) > 0:
					checkbox_list[0].click()
					print "click checkbox"
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
			if len(watch_list) >0:
				watch_json = sel.get_json(watch_list)
				vast_tag = sel.get_vast_tag(watch_json)
				print "\nWatch call response: \n" + str(json.dumps(watch_json, ensure_ascii=True)) + "\n"
				rec_len = sel.get_playlist_length(watch_list)
				print "\nTotal initial asset list: " + str(rec_len)
				if rec_len < 2:
					print "WARNING: Looks like no recs are being returned"
				elif rec_len in range(1,4):
					print "WARN: Watch call has less than 4 assets"
			secure = False
			if "https:" in url:
				dom_files = player.get_iris_files()
				if nfl and dom_files:
					assert "api-nfl.iris" in dom_files and "http://api-nfl.iris" not in dom_files, "Looks like Iris API calls are being blocked, make sure client adds Iris config ssl=true OR load as HTTP: instead"
				elif dom_files:
					assert "api.iris" in dom_files and "http://api.iris" not in dom_files, "Looks like Iris API calls are being blocked, make sure client adds Iris config ssl=true OR load as HTTP: instead"
				if len(watch_list) >=1:
					asset_url_list = sel.get_asset_urls(watch_list)
					if asset_url_list and "http:" in ','.join(asset_url_list):
						print error_messages['update feed rec']
					image_asset_list = sel.get_asset_images(watch_list)
					if image_asset_list and "http:" in ','.join(image_asset_list):
						print error_messages['update feed image']
			if not player.get_first_video():
				element = WebDriverWait(driver, timeout).until(
					wait_for_first_video(player_num)
					)
			print "\nWaiting for video to finish playing and autoplay next asset"
			for x in range(1,rec_len+1):
				player.wait_for_ad()
				if pytest.player_type == "uvpjs":
					player.wait_for_playing(playing_loc_list[0])
				temp = player.get_first_video()
				if temp and temp not in videos_played:
					videos_played.append(temp)
				player.scrub()
				element = WebDriverWait(driver, max_timeout).until(
				 		wait_for_video_to_change(player_num)
			 		)
			 	time.sleep(2)
			filter = Harfilter(proxy.har)
			watch_list = filter._filter_entries_by_url_response(iris_watch)
			watch_calls =  filter.get_matches(sel.iris_watch)
			if len(watch_list) >0:
				update_calls =  filter.get_matches(sel.iris_update)
				next_calls =  filter.get_matches(sel.iris_next)
				update_qstrings = filter._filter_return_request_querystring(iris_update)
				next_qstrings = filter._filter_return_request_querystring(iris_next)
				api_qstrings = filter._filter_return_request_querystring(api_path)
				watch_success = sel.check_single_response(watch_list)
				sel.total_calls(watch_calls,update_calls,next_calls)
				platform_id_update = sel.check_platform_id(update_qstrings)
				platform_id_next = sel.check_platform_id(next_qstrings)
				assert platform_id_update== 0, "There was " + str(platform_id_update) + " update calls missing platform_id"
				assert platform_id_next== 0, "There was " + str(platform_id_next) + " next calls missing platform_id"
				assert watch_success == True, "success did not equal true in watch call response"
				percent_watched = sel.get_percentage_watched(update_qstrings)
			print "Videos played: " + str(len(videos_played))
			assert len(watch_calls) > 0, "No watch calls logged"
			if len(videos_played) >=1 and len(videos_played) < rec_len:
				print "\nWARNING: Appears continuous playback is broken or browser/video timed out, " + str(len(videos_played)) + " videos played out of " +  str(rec_len)
			if not accounts:
				assert len(watch_calls) == expected_watch, "Extra watch calls: " + str(len(watch_calls)-1)
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
			watch_list = filter._filter_entries_by_url_response(iris_watch)
			if len(watch_list) > 0:
				response_list = filter._filter_entries_by_response(iris_watch_next)
				sel.print_responses(response_list)
				playlist = sel.get_playlist(watch_list)
				rec_ids = sel.get_json_plat_ids(playlist)
				if vast_tag:
					vast_list = filter._filter_entries_by_url_response(vast_tag)
					if not vast_list:
						print error_messages['vast tag'] + str(vast_tag)
			if len(videos_played) >=1 and rec_len > len(videos_played):
				print error_messages['playback'] + str(len(videos_played)) + " videos played out of " +  str(rec_len) 
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
				watch_qstrings = filter._filter_return_request_querystring(iris_watch)
				iris_config=sel.set_watch_call_params(watch_qstrings)
				secure = False
				if "https:" in url:
					secure = True
				if secure and not iris_config["ssl"]:
					print error_messages['ssl true']