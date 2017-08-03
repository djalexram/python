import os
import time
import pytest
from selenium import webdriver
from browsermobproxy import Server
from pyvirtualdisplay import Display
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sel


#TEST OPTIONS
timeout = 40
preroll_timeout = 60
max_timeout = 520
page_load_timeout = True
skip_forward_present = True

#OTHER VARIABLES
dir = os.getcwd()
expected_watch = 1
multiplayer = False
blank_html = 'file://' + dir + "/blank.html"
player_type="bc"


def pytest_addoption(parser):
    parser.addoption("--url", action="store", default="http://s3.amazonaws.com/iris-playground/cosmos/test_pages/qabrightcovenextgen.html", help="Test url")
    parser.addoption("--browser", action="store", default="firefox", help="Browser for test")
    parser.addoption("--headless", action="store", default="false", help="Headless boolean")
    parser.addoption("--player", action="store", default="2", help="Choose player for multiplayer")
    parser.addoption("--ads", action="store", default="false", help="Pre-roll ads boolean")

@pytest.fixture(scope='session')
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture(scope='session')
def url(request):
    return request.config.getoption("--url")

@pytest.fixture(scope='session')
def headless(request):
    return request.config.getoption("--headless")

@pytest.fixture(scope='session')
def display(request,headless):
	if headless == "true":
		d = Display(visible=0, size=(1024, 768))
		d.start()
		request.addfinalizer(lambda *args: d.stop())
		return d

@pytest.fixture(autouse=True)
def proxy(request):
	s = Server(dir+"/browsermob-proxy-2.1.4/bin/browsermob-proxy")
	s.start()
	proxy = s.create_proxy()
	proxy.new_har("player",options = {"captureHeaders": True, "captureContent": True, "captureBinaryContent": False})
	request.addfinalizer(lambda *args: s.stop())
	return proxy
 
@pytest.fixture
def driver(request, proxy,display,browser):
	d=display
	#if 'DISPLAY' not in os.environ:
	#	pytest.skip('Test requires display server (export DISPLAY)')
	httpProxy = proxy.selenium_proxy().httpProxy
	sslProxy = proxy.selenium_proxy().sslProxy
	prox = Proxy()
	prox.proxy_type = ProxyType.MANUAL
	prox.http_proxy = httpProxy
	prox.socks_proxy = httpProxy
	prox.ssl_proxy = sslProxy
	prox.autodetect = False
	if browser.lower()=="chrome":
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--proxy-server==http://%s' % httpProxy)
		chrome_options.add_argument('--ignore-certificate-errors')
		b = webdriver.Chrome(chrome_options=chrome_options)
	elif browser.lower()=="safari":
		caps = webdriver.SafariOptions()
		caps.add_argument('--proxy-server==http://%s' % httpProxy)
		b = webdriver.Safari(chrome_options=caps)
	elif browser.lower()=="edge":
		caps = webdriver.DesiredCapabilities.EDGE
		prox.add_to_capabilities(caps)
		b  = webdriver.Edge(capabilities=caps)
	elif browser.lower()=="ie":
		caps = webdriver.DesiredCapabilities.INTERNETEXPLORER
		caps['acceptInsecureCerts'] = True
		prox.add_to_capabilities(caps)
		b = webdriver.Ie(capabilities=caps)
	else:
		profile  = webdriver.FirefoxProfile()
		profile.set_proxy(prox)
		profile.accept_untrusted_certs = True
		b = webdriver.Firefox(firefox_profile=profile)
	request.addfinalizer(lambda *args: b.quit())
	return b

@pytest.fixture(autouse=True)
def selenium(driver, url):
	global multiplayer
	print url
	if page_load_timeout:
		driver.set_page_load_timeout(timeout)
		driver.get(blank_html)
		driver.execute_script('location.href = "'+ url + '"; ')
		print "waiting for page to load"
		try:
			alert = driver.switch_to_alert()
			alert.accept()
		except:
			print "no alert"
			element = WebDriverWait(driver, timeout).until(
				sel.wait_for_page_load()
				)
		print "page should be loaded"
		time.sleep(7)
	else:
		driver.get(url)
		try:
			alert = driver.switch_to_alert()
			alert.accept()
		except:
			print "no alert"
	player_type = driver.execute_script(sel.js_player_type)
	if player_type == "unknown" and page_load_timeout:
		time.sleep(10)
		player_type = driver.execute_script(sel.js_player_type)
	v= driver.execute_script(sel.js_bc_v)
	if player_type=="bc":
		iframe=""
		mute=sel.bc_mute
	elif player_type== "jw":
		iframe=""
		mute=sel.jw_mute
	elif player_type== "kmc":
		iframe=""
		mute=sel.kmc_mute
	elif player_type== "vdb":
		mute=sel.vdb_mute
		iframe=""
	elif player_type== "tp":
		iframe=""
		mute=sel.tp_mute
	elif player_type== "amp":
		iframe=""
		mute=""
	elif player_type=="oplayer":
		iframe=""
		mute=sel.o_mute
	elif player_type == "unknown":
		iframe=""
		mute=""
	if v and v != "":
		print "Player version: " + v
	print "Player type: " + player_type
	iframe_count = driver.execute_script(sel.js_get_iframe_count)
	if page_load_timeout and iframe_count >0:
		time.sleep(15)
	iframe_list = driver.find_elements_by_css_selector(sel.kmc_iframe)
	if len(iframe_list) >0:
		driver.switch_to.frame(driver.find_element_by_css_selector(sel.kmc_iframe))
		print "Switching to kmc iframe"
	elif player_type == "thePlatform":
		platform_list=driver.find_elements_by_xpath(sel.the_platform_iframe)
		if len(platform_list) >0:
			driver.switch_to.frame(driver.find_element_by_xpath(sel.the_platform_iframe))
			print "Switching to iframe: " + sel.the_platform_iframe
	else:
		iframe_num = driver.execute_script(sel.js_get_iframe)
		if iframe_num and iframe_num != "":
			iframe = "(//iframe)[" + str(iframe_num) + "]"
			driver.switch_to.frame(driver.find_element_by_xpath(iframe))
			print "Switching to iframe: " + iframe
	playing_list = driver.find_elements_by_css_selector(sel.pause)
	if len(playing_list) >= 2:
		driver.execute_script("arguments[0].click();", playing_list[1])
		print "Pausing second player, we recommend auto-play be disabled thru Brightcove since extra API calls will be introduced by second player causing tests to fail"
	driver.execute_script(sel.js_play)
	if multiplayer == True:
		driver.execute_script(sel.js_play2)
	p_list = driver.find_elements_by_css_selector(sel.play2)
	if len(p_list) > 0 and p_list[0].is_displayed():
		p_list[0].click()
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

@pytest.fixture(autouse=True)
def myglobal(request):
    request.function.func_globals['expected_watch'] = expected_watch
    request.function.func_globals['max_timeout'] = max_timeout
    request.function.func_globals['timeout'] = timeout
    request.function.func_globals['player_type'] = player_type

# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     # execute all other hooks to obtain the report object
#     outcome = yield
#     rep = outcome.get_result()
#     # we only look at actual failing test calls, not setup/teardown
#     if rep.when == "call" and rep.failed:
#     	selenium.save_screenshot(sel.get_screenshot_filename())
#     elif call.excinfo:
#     	selenium.save_screenshot(sel.get_screenshot_filename())






