from browsermobproxy import Server   
from filter import Harfilter
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import ast
import json
import time
import sel

server = Server(sel.browsermob_path)

try:
	server.start()

	proxy = server.create_proxy()
	from selenium import webdriver
	profile  = webdriver.FirefoxProfile()
	profile.set_proxy(proxy.selenium_proxy())
	driver = webdriver.Firefox(firefox_profile=profile)
	proxy.new_har("player",options = {"captureHeaders": True, "captureContent": True, "captureBinaryContent": False})
	driver.implicitly_wait(11)
	driver.get(sel.url)
	time.sleep(25)
	filter = Harfilter(proxy.har)
	iris_files = filter._filter_return_url(sel.iris_path)
	iris_403 = filter._filter_return_error(sel.iris_path, 403)
	iris_404 = filter._filter_return_error(sel.iris_path, 404)
	iris_500 = filter._filter_return_error(sel.iris_path, 500)
	combined_irisfiles = '\t'.join(iris_files)

	print "IRIS FILES REQUESTED" 
	for i in iris_files:
		print i
	if '.css' not in combined_irisfiles:
		print "No Iris CSS was loaded (not added to HTML source code)\n"
	assert  len(iris_403) == 0, "Some Iris files failed w/ 403 error:\n" + str(iris_403)
	assert  len(iris_404) == 0, "Some Iris files failed w/ 404 error:\n" + str(iris_404)
	assert  len(iris_500) == 0, "\nSome Iris files failed w/ 500 error:\n" + str(iris_500)
	assert '.js' in combined_irisfiles, "Iris JS file missing\n"
	
	element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, sel.forward_xpath))
    )
	driver.execute_script(sel.js_forward)
	element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, sel.forward_xpath))
    )
	#result = json.dumps(proxy.har, ensure_ascii=False)
	#har_file = open('requests' + str(int(time.time())) + '.har', 'w')
	#har_file.write(result.encode('utf-8'))
	#har_file.close()
	filter = Harfilter(proxy.har)
	api_404 = filter._filter_return_error(sel.iris_api, 404)
	api_500 = filter._filter_return_error(sel.iris_api, 500)

	watch_calls =  filter.get_matches(sel.iris_watch)
	update_calls =  filter.get_matches(sel.iris_update)
	next_calls =  filter.get_matches(sel.iris_next)
	playerList = filter._filter_entries_by_url_response(sel.iris_watch)

	update_queryStrings = filter._filter_return_request_querystring(sel.iris_update);
	
	tempJson = json.dumps(update_queryStrings, ensure_ascii=True)
	tempJson = json.loads(tempJson)
	
	sel.getUpdateCalls(tempJson)
	#print "\nPlatform id: " + tempJson[0]["platform_id"]
	#print "Asset title: " + tempJson[0]["title"]
	#print "Perecent watched: " + tempJson[0]["behavior[percentage_watched]"]
	assert  tempJson[0]["behavior[next]"] == "1", "behavior[next] did not equal 1"

	print "\nTotal watch calls " + str(len(watch_calls))
	print "Total update calls " + str(len(update_calls))
	print "Total next calls " + str(len(next_calls))

	assert  len(iris_404) == 0, "Some Iris API calls failed w/ 404 error: " + str(api_404)
	assert  len(iris_500) == 0, "\nSome Iris API calls failed w/ 500 error: " + str(api_500)

finally:
	server.stop()
	driver.quit()