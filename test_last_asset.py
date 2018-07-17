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
class TestLastAsset(object):
	def test_next_calls_after_last_asset(self,selenium,proxy,preroll_ads,skip_forward_present,accounts,player_num,data,env,log,check_player_url,api_test):
		#NOTE once the last asset is reached it will not play any more videos since it will not play duplicates
		api_path = pytest.iris_api
		videos_played = []
		asset_len = []
		iris_config = dict()
		try:
			driver = selenium
			player = Player(driver,timeout,preroll_ads,player_num)
			player.wait_for_ad()
			if skip_forward_present:
				player.wait_for_forward()
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
			jsonObj = sel.get_json(watch_list)
			watch_success = sel.check_single_response(watch_list)
			playlist = sel.get_playlist(watch_list)
			experience = jsonObj["experience"]
			print "\nExperience: " + experience
			y=len(jsonObj["next"])
			asset_len = y
			print "\nTotal initial asset list: " + str(y)
			if y < 2:
				print "WARNING: Looks like no recs are being returned"
			elif y in range(1,4):
				print "WARNING: Watch call has less than 4 assets"
			#y=int(playerListLen)
			last_platform_id = playlist[y-1]["platform_id"]
			print "Last asset platform_id: " + last_platform_id
			for x in range(y+3):
				if x+1==y:
					filter = Harfilter(proxy.har)
					next_calls =  filter.get_matches(sel.iris_next)
					temp_update =  filter.get_matches(sel.iris_update)
					last_update = len(temp_update)-1
				temp = player.get_first_video()
				if temp and temp not in videos_played:
					videos_played.append(temp)
				player.click_forward()
				player.wait_for_ad()
				player.wait_for_forward
				time.sleep(2)
			filter = Harfilter(proxy.har)
			next_calls2 =  filter.get_matches(sel.iris_next)
			#print  "Additional next calls after last asset: " + str(len(next_calls2) - len(next_calls))
			print "Videos played: " + str(len(videos_played))
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
			if secure and not sel.ssl:
				print "Make sure client adds Iris config ssl=true OR load as HTTP: instead"
			if platform_id_update> 0 or platform_id_next> 0:
				print "\nWatch call response: \n" + str(json.dumps(sel.get_json(watch_list), ensure_ascii=True)) + "\n"
			assert platform_id_update== 0, "There was " + str(platform_id_update) + " update calls missing platform_id"
			assert platform_id_next== 0, "There was " + str(platform_id_next) + " next calls missing platform_id"
			experience_update = sel.check_experience(experience,update_qstrings)
			experience_next = sel.check_experience(experience,next_qstrings)

			assert experience_update== 0, "There was " + str(experience_update) + " update calls with different experience"
			assert experience_next== 0, "There was " + str(platform_id_next) + " next calls with different experience"
			assert len(next_calls2) <= len(next_calls) + 2, "Too many /next calls after last asset played"
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
				response_list = filter._filter_entries_by_response(iris_watch_next)
				sel.print_responses(response_list)
				watch_calls =  filter.get_matches(sel.iris_watch)
				if len(watch_calls) > 1:
					print "\nWARNING: Something doesnt look correct, there was more than 1 watch call"
			apiErrors = filter._filter_return_errors(api_path)
			if api_test:
				assert len(apiErrors) == 0, error_messages['api error']
			watch_list = filter._filter_entries_by_url_response(sel.iris_watch)
			iris_files = filter._filter_return_url_from_list(iris_scripts)
			httpErrors = filter._filter_return_errors(iris_prod)
			watch_json = sel.get_json(watch_list)
			sel.get_vast_tag(watch_json)
			if len(iris_files) >0:
				print "\nIris files:"
				for x in iris_files:
					print x
			if len(iris_files) >0 and '.js' not in sel.check_iris_files(iris_files):
				print "Iris JS file missing\n"
			if len(videos_played) >=1 and len(videos_played) < asset_len:
				print error_messages['playback'] + str(len(videos_played)) + " videos played out of " +  str(asset_len) 
			jwErrors = filter._filter_return_errors(jw_feed)
			if len(jwErrors) >0:
				print error_messages['jw feed']
			bcovErrors = filter._filter_return_errors(bcov_cms)
			if len(bcovErrors) >0:
				print error_messages['bcov cms']
				print error_messages['video not found'] + str(sel.get_cms_ids(bcovErrors))
			if env == "prod" and len(watch_list) > 0:
				playlist = sel.get_playlist(watch_list)
				next_list = filter._filter_entries_by_url_response(iris_next)
				if check_player_url and len(next_list) > 0:
					dup_recs = sel.check_for_dup_recs(playlist,next_list)
					if dup_recs and len(dup_recs) > 1:
						print error_messages['dup recs'] + ", platform id(s): " + str(dup_recs)
				assert sel.check_for_dup_asset(playlist) == False, error_messages['dup asset']

	def last_asset_platform_id_passed(self,selenium,proxy,preroll_ads,skip_forward_present,accounts,player_num,env,log):
		#This can only be run for certain test pages where it stops playing videos after initial playlist
		#Test to check for platform_id from last asset passed for remaining update calls
		#NOTE once the last asset is reached it will not play any more videos since it will not play duplicates
		videos_played = []
		asset_len = []
		iris_config = dict()
		try:
			driver = selenium
			time.sleep(5)
			player = Player(driver,timeout,preroll_ads,player_num)
			if skip_forward_present:
				player.wait_for_forward()
			player.wait_for_ad()
			time.sleep(3)
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
			playlist = sel.get_playlist(watch_list)
			y=len(jsonObj["next"])
			asset_len = y
			print "\nTotal initial asset list: " + str(y)
			#y=int(playerListLen)
			last_platform_id = playlist[y-1]["platform_id"]
			print "Last asset platform_id: " + last_platform_id
			for x in range(y+3):
				if x+1==y:
					filter = Harfilter(proxy.har)
					next_calls =  filter.get_matches(sel.iris_next)
					temp_update =  filter.get_matches(sel.iris_update)
					last_update = len(temp_update)-1
				temp = player.get_first_video()
				if temp and temp not in videos_played:
					videos_played.append(temp)
				player.click_forward()
				time.sleep(3)
			print "Videos played: " + str(len(videos_played))
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
			for x in range(last_update,len(update_qstrings)):
				temp_plat = update_qstrings[x].get("platform_id","")
				if not accounts:
					assertTrue(temp_plat == last_platform_id, "platform_id:" + last_platform_id + " for last asset was not passed for remaining api calls, this was passed instead: " + temp_plat)
			platform_id_update = sel.check_platform_id(update_qstrings)
			platform_id_next = sel.check_platform_id(next_qstrings)
			next_list = filter._filter_entries_by_url_response(sel.iris_next)
			if len(next_list) > 0:
				next_success_total = sel.check_response(next_list)
				assert next_success_total == 0, "Some next calls did not contain \"success\":true, " + next_success_total + " calls"
			assert platform_id_update== 0, "There was " + str(platform_id_update) + " update calls missing platform_id"
			assert platform_id_next== 0, "There was " + str(platform_id_next) + " next calls missing platform_id"
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