import pytest
import requests  
from filter import Harfilter
from sel import Player,wait_for_video_to_change, wait_for_first_video,wait_for_page_load
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locators import PlayerLocators
from selenium import webdriver

import ast
import json
import time
import sel
import sys

@pytest.mark.setup
class TestRecsExists(object):

	def test_recs_exists(self,selenium,proxy,preroll_ads,skip_forward_present,accounts,player_num,env,data,log, check_player_url,api_test):
		videos_played =[]
		rec_len = 0
		api_path = pytest.iris_api
		try:
			driver=selenium
			player = Player(driver,timeout,preroll_ads,player_num)
			player_error = player.check_for_error(path)
			player.wait_for_ad()
			player.check_if_paused()
			assert player_error == False, "Player Error: " + player_error
			if skip_forward_present:
				player.wait_for_forward()
			url = driver.current_url
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
			url = driver.current_url
			secure = False
			if "https:" in url:
				dom_files = player.get_iris_files()
				if nfl and dom_files:
					assert "api-nfl.iris" in dom_files and "http://api-nfl.iris" not in dom_files, "Iris API calls are being blocked, make sure client adds Iris config ssl=true OR load as HTTP: instead"
				elif dom_files:
					assert "api.iris" in dom_files and "http://api.iris" not in dom_files, "Iris API calls are being blocked, make sure client adds Iris config ssl=true OR load as HTTP: instead"
				if len(watch_list) >=1:
					asset_url_list = sel.get_asset_urls(watch_list)
					if asset_url_list and "http:" in ','.join(asset_url_list):
						print error_messages['update feed rec']
					image_asset_list = sel.get_asset_images(watch_list)
					if image_asset_list and "http:" in ','.join(image_asset_list):
						print error_messages['update feed image']
			assert len(watch_list) > 0, "Watch call was not made in alloted time"
			jsonObj = sel.get_json(watch_list)
			print "\nTotal initial asset list: " + str(len(jsonObj["next"]))
			watch_success = sel.check_single_response(watch_list)
			recs = sel.get_asset_urls(watch_list)
			flag = True
			failed = []
			for r in recs:
				if r and r != "" and "http" in r:
					temp = requests.head(r)
					rec_status = temp.status_code
					if rec_status != 200 and rec_status >= 400:
						failed.append(r)
						flag = False
						print "\nFile failed to load w/ status " + str(rec_status) + "\n" + r
					elif rec_status in range (300,400):
						print "\nAsset URL appears to be redirect " + str(rec_status) + "\n" + r
			if flag:
				print "Looks like all recs/assets are valid"
			assert len(failed) == 0, "Some recs/assets are not valid or do not exist, results may not be accurate if assets are geo-blocked"
			

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
				assert len(apiErrors) == 0
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
				response_list = filter._filter_entries_by_response(iris_watch_next)
				sel.print_responses(response_list)
				playlist = sel.get_playlist(watch_list)
				rec_ids = sel.get_json_plat_ids(playlist)
				watch_json = sel.get_json(watch_list)
				sel.get_vast_tag(watch_json)
				if sel.watch_platform_id in rec_ids:
					rec_len = rec_len -1
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
				watch_qstrings = filter._filter_return_request_querystring(sel.iris_watch)
				sel.set_watch_call_params(watch_qstrings)
				secure = False
				if "https:" in url:
					secure = True
				if secure and not sel.ssl:
					print error_messages['ssl true']