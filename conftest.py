import os
import shlex, subprocess
import time
import importlib
import pytest
#from selenium import webdriver
from browsermobproxy import Server
from pyvirtualdisplay import Display
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException, TimeoutException
import sel
from locators import iframe_loc_list, play_list


#TEST OPTIONS
timeout = 60
max_timeout = 530
load_timeout = 60
ads_present = False
player_url = "http://s3.amazonaws.com/iris-playground/cosmos/test_pages/qabrightcovenextgen.html"


#OTHER VARIABLES
iris_prod = "ovp.iris.tv"
iris_api = 'api.iris.tv'
nfl_api = "api-nfl.iris.tv"
iris_watch = 'iris.tv/watch'
iris_update = 'iris.tv/update'
iris_next = 'iris.tv/next'
bcov_ima3= 2.21
bcov_player = "players.brightcove.net/"
iris_watch_next = [iris_watch, iris_next]
iris_scripts = [iris_prod,"s3.amazonaws.com/iris-playground/cosmos/libs","s3.amazonaws.com/iris-playground/cosmos/plugins","s3.amazonaws.com/iris-playground/cosmos/styles","iris.adaptive.js"]
jw_feed = "content.jwplatform.com/feeds/"
bcov_cms = "edge.api.brightcove.com/playback/v1/accounts/"
path = os.getcwd()
api_watch = "http://api.iris.tv/watch?number=5&base_url=defaultbaseurl&client_token=1736779881001&platform=brightcove&access_token=1d9f05c8b00daddfbffcf5afa8a0691bf6370c0cd9dfc8bc6fb38e13c4474dab&ssl=false&platform_id=4329281781001&player_version=Brightcove.Nextgen&disable_mobile_upnext=false&up_next_min_vid_length=23&start_up_next=true&start_up_next_text=UP-NEXT&start_up_next_time=5&start_up_next_length=7&end_up_next=true&end_up_next_text=RECOMMENDED&end_up_next_time=5&end_up_next_length=7&player_id=myPlayer&campaign_tracking=true&side_rail=false&related_rail=false&set_cookie=true&user_id=UP-DpRtIjxqforfAgA&callback=superagentCallback1526422963360469"
expected_watch = 1
multiplayer = False
blank_html = 'file://' + path + "/blank.html"
chrome_apk = path+"/apk/chrome_64.0.3282.137-328213711-x86.apk"
pytest.player_type=None
env_var="qa"
anvato_loc = "iframe[id='anv_player']"
url_env="prod"
stage_url = "s3.amazonaws.com/iris-playground"
proxy_enabled = ["firefox","ff","chrome","andriod","chrome:nexus7","chrome:nexus6p","ie"]
stage_players = "http://s3.amazonaws.com/iris-playground/cosmos/test_pages/qabrightcovenextgen.html","http://s3.amazonaws.com/iris-playground/cosmos/test_pages/jwplayer.html","http://www.kaltura.com/index.php/extwidget/preview/partner_id/1344571/uiconf_id/38056231/entry_id/0_42qi7rzj/embed/dynamic?&flashvars[streamerType]=auto"
prod_players = "http://s3.amazonaws.com/iris-playground/cosmos/test_pages/prodbrightcovenextgen.html","http://s3.amazonaws.com/iris-playground/cosmos/test_pages/prod-jwplayer.html"
error_messages = {'api error':'Test failed due to API errors','jw feed':'\nWARNING: Looks like there was problem loading asset/feed from JW, this may cause playback issues','bcov cms':'\nWARNING: Looks like there was problem loading asset(s) from Brightcove CMS, this may cause playback issues', 'dup asset':"\nContact Zac, watch call contains duplicate asset, potentially due to recency weight", 'ssl true':"\nMake sure client adds Iris config ssl=true OR load as HTTP: instead", 'vast tag':"\nWARNING: Looks like vast tag was not fired", 'playback':"\nWARNING: Appears continuous playback is broken or browser/video timed out, ", 'video not found':"\nThe following platform ids are returnning video not found error\n", 'update feed rec':"\nWARNING: Client should update feed with all video content_url as HTTPS if they expect playback on website with HTTPS", 'api blocked':"\nIris API calls are being blocked, make sure client adds Iris config ssl=true OR load site as HTTP: instead", 'update feed image':"\nWARNING: If Upnext images are not loading, client should update feed with all thumbnail images as HTTPS", 'dup recs':"\nWARNING: Next call contained duplicate recs from initial watch call, make sure taxonomy is setup"}


def pytest_addoption(parser):
    parser.addoption("--url", action="store", default=player_url, help="Test url")
    parser.addoption("--ec2", action="store", default=iris_api, help="domain")
    parser.addoption("--browser", action="store", default="chrome", help="Browser for test")
    parser.addoption("--headless", action="store", default=False, help="Headless boolean")
    parser.addoption("--player", action="store", default="1", help="Choose player for multiplayer")
    parser.addoption("--timeout", action="store", default=timeout, help="Timeout for test")
    parser.addoption("--ads", action="store", default=ads_present, help="Pre-roll ads boolean")
    parser.addoption("--skip", action="store", default=True, help="Skip forward present boolean")
    parser.addoption("--accounts", action="store", default=False, help="Executed by accounts tool boolean")
    parser.addoption("--env", action="store", default=env_var, help="Environment")
    parser.addoption("--api_test", action="store", default=False, help="Api Test")
    parser.addoption("--blog", action="store", default=False, help="Option to store browser logs")
    parser.addoption("--mobile", action="store", default=False, help="Determine mobile")
    parser.addoption("--watch", action="store", default=api_watch, help="Watch call")

@pytest.fixture(scope='session')
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture(scope='session')
def api_test(request):
    return request.config.getoption("--api_test")

@pytest.fixture(scope='session')
def ec2(request):
    return request.config.getoption("--ec2")

@pytest.fixture(scope='session')
def mobile(request,browser):
    if browser.lower() in ['ipad','andriod']:
    	#webdriver = importlib.import_module('appium.webdriver')
    	return True
    else:
    	#webdriver = importlib.import_module('selenium.webdriver')
    	return request.config.getoption("--mobile")

@pytest.fixture(scope='session')
def webdriver(request,mobile):
	if mobile:
		w = importlib.import_module('appium.webdriver')
	else:
		w = importlib.import_module('selenium.webdriver')
	return w

@pytest.fixture(scope='session')
def log(request, browser):
	temp = request.config.getoption("--blog")
	if not temp and "chrome" in browser:
		temp = str(int(time.time())) + ".log"
	return temp

@pytest.fixture(scope='session')
def accounts(request):
    return request.config.getoption("--accounts")

def pytest_configure(config):
    config._metadata['Browser'] = config.getoption("browser")

def pytest_generate_tests(metafunc):
    if 'url' in metafunc.fixturenames:
        if metafunc.config.getoption('env') == "stage":
            metafunc.parametrize("url", stage_players)
        elif metafunc.config.getoption('env') == "prod":
        	metafunc.parametrize("url", prod_players)

@pytest.fixture(scope='session')
def url(request):
	return request.config.getoption("--url")

@pytest.fixture(scope='session')
def watch_call(request,ec2):
	if ec2 != iris_api:
		return "http://" + ec2 + "/watch?number=5&base_url=defaultbaseurl&client_token=1736779881001&platform=brightcove&access_token=1d9f05c8b00daddfbffcf5afa8a0691bf6370c0cd9dfc8bc6fb38e13c4474dab&ssl=false&platform_id=4329281781001&player_version=Brightcove.Nextgen&disable_mobile_upnext=false&up_next_min_vid_length=23&start_up_next=true&start_up_next_text=UP-NEXT&start_up_next_time=5&start_up_next_length=7&end_up_next=true&end_up_next_text=RECOMMENDED&end_up_next_time=5&end_up_next_length=7&player_id=myPlayer&campaign_tracking=true&side_rail=false&related_rail=false&set_cookie=true&user_id=UP-DpRtIjxqforfAgA&callback=superagentCallback1526422963360469"
	else:
		return request.config.getoption("--watch")

@pytest.fixture()
def check_player_url(request,url):
	if "s3.amazonaws.com/iris-playground" in url:
		return False
	else:
		return True


@pytest.fixture(scope='session')
def preroll_ads(request):
	return request.config.getoption("--ads")

@pytest.fixture(scope='session')
def env(request):
	return request.config.getoption("--env")


@pytest.fixture(scope='session')
def skip_forward_present(request):
	s= request.config.getoption("--skip")
	if str(s).lower() != "true":
		return False
	else:
		return s

@pytest.fixture(scope='session')
def player_num(request):
	return int(request.config.getoption("--player"))

@pytest.fixture(scope='session')
def headless(request):
    return request.config.getoption("--headless")

@pytest.fixture(scope='session')
def timeout_f(request):
    return request.config.getoption("--timeout")

def pytest_runtest_setup(item):
	if item.config.getoption("--browser") == "safari" and item.config.getoption("-m") == "regression":
            pytest.skip("test requires driver that supports proxy")

@pytest.fixture(scope='session')
def display(request,headless):
	if headless:
		d = Display(visible=0, size=(1024, 768))
		d.start()
		request.addfinalizer(lambda *args: d.stop())
		return d

@pytest.fixture(scope='session')
def server(request,browser):
	if browser.lower() in proxy_enabled:
		s = Server(path+"/browsermob-proxy-2.1.4/bin/browsermob-proxy")
		s.start()
		request.addfinalizer(lambda *args: s.stop())
	else:
		s=False
	return s

@pytest.fixture(scope="session")
def proxy(request,server,browser):
	if server:
		if browser.lower() == "andriod":
			proxy = server.create_proxy({"port":8097,'trustAllServers':'true'})
		else:
			proxy = server.create_proxy({'trustAllServers':'true'})
		def fin():
			proxy.close()
			print "Closing proxy"
		request.addfinalizer(lambda *args: fin)
		return proxy
	else:
		return False

@pytest.fixture()
def proxy_har(proxy):
	if proxy:
		proxy.new_har("player",options = {"captureHeaders": True, "captureContent": True, "captureBinaryContent": False})
 
@pytest.fixture
def driver(request, proxy,display,browser,log,proxy_har,url, webdriver):
	d=display
	#if 'DISPLAY' not in os.environ:
	#	pytest.skip('Test requires display server (export DISPLAY)')
	prox = Proxy()
	if proxy:
		httpProxy = proxy.selenium_proxy().httpProxy
		sslProxy = proxy.selenium_proxy().sslProxy
		prox.proxy_type = ProxyType.MANUAL
		prox.http_proxy = httpProxy
		prox.socks_proxy = httpProxy
		prox.ssl_proxy = sslProxy
		prox.autodetect = False
		proxy_har
	if "chrome" in browser.lower():
		caps = webdriver.DesiredCapabilities.CHROME.copy()
		chrome_options = webdriver.ChromeOptions()
		prefs = {"profile.default_content_setting_values.plugins":1, "profile.content_settings.plugin_whitelist.adobe-flash-player":1,
		"profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player":1,"PluginsAllowedForUrls":url}
		chrome_options.add_experimental_option("prefs", prefs)
		m = browser.lower().split(":")
		if len(m) > 1:
			if m[1] == "nexus7":
				mobile_emulation = { "deviceName": "Nexus 7" }
			elif m[1] == "nexus6p":
				mobile_emulation = { "deviceName": "Nexus 6P" }
			chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
		chrome_options.add_argument('--proxy-server==http://%s' % httpProxy)
		chrome_options.add_argument('--ignore-certificate-errors')
		chrome_options.add_argument('--dns-prefetch-disable')
		caps['loggingPrefs'] = { 'browser':'ALL' }
		caps['acceptInsecureCerts'] = True
		#chrome_options.addArguments("--disable-web-security")
		#chrome_options.addArguments("--allow-running-insecure-content");
		b = webdriver.Chrome(desired_capabilities = caps, chrome_options=chrome_options,service_args=["--verbose", "--log-path="+ path +"/browser_logs/"+ log])
	#Safari webdriver currently does not support proxy
	elif "safari" in browser.lower():
		m = browser.lower().split(":")
		if len(m) > 1:
			if m[1] == "ipad":
				command_line = "defaults write com.apple.Safari CustomUserAgent \"\\\"Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X; en-us) AppleWebKit/534.46 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53\\\"\""
				args = shlex.split(command_line)
				subprocess.Popen(args)
			elif m[1] == "iphone":
				command_line = "defaults write com.apple.Safari CustomUserAgent \"\\\"Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_1_2 like Mac OS X; de-de) AppleWebKit/528.18 (KHTML, like Gecko) Mobile/7D11\\\"\""
				args = shlex.split(command_line)
				subprocess.Popen(args)
		caps = webdriver.DesiredCapabilities.SAFARI.copy()
		#prox.add_to_capabilities(caps)
		b = webdriver.Safari(desired_capabilities=caps)
	#Edge webdriver currently does not support proxy
	elif browser.lower()=="edge":
		caps = webdriver.DesiredCapabilities.EDGE.copy()
		#prox.add_to_capabilities(caps)
		b  = webdriver.Edge(capabilities=caps)
	elif browser.lower()=="ie":
		caps = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
		caps['ie.usePerProcessProxy'] = True
		caps['ie.setProxyByServer'] = True
		caps['unexpectedAlertBehaviour'] = 'accept'
		caps['acceptInsecureCerts'] = True
		caps['proxy'] = {"proxyType":"manual", "socksProxy":httpProxy, "httpProxy":httpProxy, "sslProxy":httpProxy}
		#b = webdriver.Ie(service_args=["--log-level=DEBUG"],capabilities=caps)
		b = webdriver.Ie(capabilities=caps)
	elif browser.lower()=="ipad":
		capabilities = { 'automationName':'XCUITest','platformName': 'iOS', 'platformVersion': '10.0',"nativeWebTap": True, 'deviceName': 'iPad Air','showXcodeLog': True,'browserName': 'safari',"xcodeOrgId": "<Team ID>",
      "xcodeSigningId": "iPhone Developer"}
		b = webdriver.Remote('http://localhost:4723/wd/hub', capabilities)
	elif browser.lower()=="andriod":
		capabilities = { 'platformName': 'Android', 'platformVersion': '7.0','deviceName': 'Android Emulator','browserName': 'Chrome', 'app': chrome_apk}
		b = webdriver.Remote('http://localhost:4723/wd/hub', capabilities)
	else:
		caps = webdriver.DesiredCapabilities.FIREFOX.copy()
		caps['loggingPrefs'] = { 'browser':'SEVERE' }
		caps['acceptInsecureCerts'] = True
		profile  = webdriver.FirefoxProfile()
		profile.set_proxy(prox)
		profile.accept_untrusted_certs = True
		profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','true')
		b = webdriver.Firefox(capabilities=caps, firefox_profile=profile)
	request.addfinalizer(lambda *args: b.quit())
	return b

@pytest.fixture()
def selenium(request, driver, browser,player_num,url,check_player_url):
	global multiplayer
	print url
	timedout=False
	v = False
	ima3 = False
	freewheel = False
	iframe_count = False
	iframe_elem = None
	try:
		driver.set_page_load_timeout(load_timeout)
		driver.get(url)
	except TimeoutException:
		print "browser load timeout"
		timedout = True
	if timedout:
		try:
			element = WebDriverWait(driver, timeout+15).until(
				sel.wait_for_page_load()
			)
		except TimeoutException:
			print "Second browser load timeout"
		#driver.execute_script("window.stop();") 
	try:
		alert = driver.switch_to_alert()
		alert.accept()
		iframe_count = driver.execute_script(sel.js_get_iframe_count)
	except:
		print "no alert"
	#add delay to wait for dynamically inserted iframes
	if iframe_count and int(iframe_count) ==0:
		time.sleep(3)
	iframe = False
	driver.implicitly_wait(0.25)
	for iframe_loc in iframe_loc_list:
		iframe_list = driver.find_elements_by_css_selector(iframe_loc)
		if iframe_list and player_num > 1 and iframe_list[player_num-1]:
			iframe_elem = iframe_list[player_num-1]
			if player_num >1:
				player_num = 1
			iframe = iframe_loc
			print "Switching to iframe: " + iframe_loc
			driver.switch_to.frame(iframe_elem)
			break
		elif iframe_list and iframe_list[0]:
			iframe_elem = iframe_list[0]
			iframe = iframe_loc
			print "Switching to iframe: " + iframe_loc
			driver.switch_to.frame(iframe_elem)
			break
	if not iframe:
		iframe_num = driver.execute_script(sel.js_get_iframe)
		if iframe_num and iframe_num != "":
			iframe_xpath = "(//iframe)[" + str(iframe_num) + "]"
			xframe = driver.find_element_by_xpath(iframe_xpath)
			print "Switching to iframe: " + iframe_xpath
			driver.switch_to.frame(xframe)
	playing_list = driver.find_elements_by_css_selector(sel.pause)
	if len(playing_list) >= 2:
		driver.execute_script("arguments[0].click();", playing_list[1])
		print "Pausing second player, we recommend auto-play be disabled since extra API calls will be introduced by second player causing tests to fail"
	mplayer = sel.Multiplayer(player_num)
	try:
		pytest.player_type = driver.execute_script(sel.js_player_type)
	except:
		print "probably TimeoutException, not able to detect player type"
	if driver.execute_script(sel.js_is_amp) and not check_player_url:
		driver.refresh()
		try:
			element = WebDriverWait(driver, timeout+15).until(
				sel.wait_for_page_load()
			)
		except TimeoutException:
			print "browser load timeout"
	playing = driver.execute_script(sel.js_playing_state)
	if not playing :
		print "looking for play button"
		for p in play_list:
			fplay = driver.find_elements_by_css_selector(p)
			if fplay and fplay[0].is_displayed():
				try:
					fplay[0].click()
					print "play button clicked"
				except:
					print "Found play button but was not able to click on it"
				break
	if iframe == anvato_loc:
		print "Switching to main window"
		driver.switch_to.default_content()
	driver.execute_script(sel.js_mute)
	if iframe == anvato_loc:
		print "Switching back to iframe"
		driver.switch_to.frame(iframe_elem)
	if multiplayer == True:
		driver.execute_script(sel.js_play2)
	try:
		v= driver.execute_script(sel.js_bc_v)
	except:
		print "probably TimeoutException, not able to detect BCOV version"
	if "safari" in browser and browser != "safari":
		try:
			print "User Agent: " + driver.execute_script(sel.js_get_ua)
		except:
			print "probably TimeoutException"
	mute=""
	if pytest.player_type=="bc":
		if v and v != "":
			print "Brightcove player version: " + v
	elif pytest.player_type== "kmc":
		mute=sel.kmc_mute
	elif pytest.player_type== "vdb":
		mute=sel.vdb_mute
	elif pytest.player_type== "tp":
		mute=sel.tp_mute
	elif pytest.player_type=="oplayer":
		mute=sel.o_mute
	elif pytest.player_type=="thePlatform":
		mute=sel.platform_mute
	print "Player type: " + pytest.player_type
	try:
		ima3 = driver.execute_script(sel.js_get_ima3)
		if ima3:
			print "Brightcove ima3 version: " + ima3
	except:
		print "exception"
	try:
		ad_plat= driver.execute_script(sel.js_ad_platform)
		if ad_plat:
			print "Ad platform: " + ad_plat
	except:
		print "probably TimeoutException, not able to detect ad platform"
	try:
		freewheel = driver.execute_script(sel.js_get_freewheel)
	except: 
		print "exception"
	if freewheel:
		print "Brightcove Freewheel version: " + freewheel
	if mute != "":
		mute_list = driver.find_elements_by_xpath(mute)
		if len(mute_list) > 0:
			element = driver.find_element_by_xpath(mute)
			driver.execute_script("arguments[0].click();", element)
		if len(mute_list) >=2:
			driver.execute_script("arguments[0].click();", mute_list[1])
	# if player_type == "vdb":
	# 	driver.switch_to.default_content()
	if len(driver.find_elements_by_css_selector(sel.play)) >= 2:
		multiplayer = False
	if multiplayer == True and expected_watch==1:
		expected_watch = expected_watch * 2
	driver.implicitly_wait(11)

	return driver

@pytest.fixture
def data():
    pytest.iris_api = iris_api


@pytest.fixture(autouse=True)
def myglobal(request,timeout_f):
    request.function.func_globals['expected_watch'] = expected_watch
    request.function.func_globals['max_timeout'] = max_timeout
    request.function.func_globals['timeout'] = timeout_f
    request.function.func_globals['path'] = path
    request.function.func_globals['iris_scripts'] = iris_scripts
    request.function.func_globals['iris_prod'] = iris_prod
    request.function.func_globals['iris_watch'] = iris_watch
    request.function.func_globals['iris_next'] = iris_next
    request.function.func_globals['iris_update'] = iris_update
    request.function.func_globals['iris_api'] = iris_api
    request.function.func_globals['nfl_api'] = nfl_api
    request.function.func_globals['jw_feed'] = jw_feed
    request.function.func_globals['bcov_cms'] = bcov_cms
    request.function.func_globals['bcov_player'] = bcov_player
    request.function.func_globals['iris_watch_next'] = iris_watch_next
    request.function.func_globals['stage_url'] = stage_url
    request.function.func_globals['anvato_loc'] = anvato_loc
    request.function.func_globals['error_messages'] = error_messages

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item,call):
    #_driver = item.funcargs['selenium']
    #browser_type = _driver.capabilities['browserName']
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call':
        if "url" in item.fixturenames:
        	extra.append(pytest_html.extras.url(item.funcargs["url"]))
        #screenshot = _driver.get_screenshot_as_base64()
        #extra.append(pytest_html.extras.image(screenshot, ''))
        report.extra = extra