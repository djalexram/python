import os
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from pyvirtualdisplay import Display
from locators import PlayerLocators
import time
import json

#TEST OPTIONS
browser="firefox"
headless = False
timeout = 40
preroll_timeout = 60
max_timeout = 520
page_load_timeout = True
skip_forward_present = True
preroll_ads = True

#Other variables
dir = os.getcwd()
browsermob_path = dir+"/browsermob-proxy-2.1.4/bin/browsermob-proxy"
urls_path = dir+"/urls.json"
blank_html = 'file://' + dir + "/blank.html"
chrome_apk = dir+"/apk/com.android.chrome_58.0.3029.83-302908310-x86.apk"
iris_path = 's3.amazonaws.com/iris-playground'
iris_js = 'iris.adaptive.js'
iris_api = 'api.iris.tv'
iris_watch = 'iris.tv/watch'
iris_update = 'iris.tv/update'
iris_next = 'iris.tv/next'
bc_play="(//button[@class='vjs-big-play-button'])[1]"
chrome_termsID="terms_accept"
player='bc'
iframe=""
mute=""
ver=""
video1=""
expected_watch = 1
frame_kmc="kaltura_player_ifp"
kmc_iframe = "iframe[class*='EmbedKalturaIframe']"
campaign_tracking=False
multiplayer = False
start_up_next_text=""
end_up_next_text=""
start_up_next=True
end_up_next=True
player_error = "Setup Timeout Error: Setup took longer than 30 seconds to complete"
appium_url = 'http://s3.amazonaws.com/iris-playground/cosmos/test_pages/brightcovenextgen.html'
browsermob_options = '{"captureHeaders": True, "captureContent": True, "captureBinaryContent": False}'
forward_xpath = "//*[contains(@id,'skip_forward')]"
forward_xpath2 = "(//*[contains(@id,'skip_forward')])[2]"
forward = "div[class*='skip_forward']"
back_xpath = "//*[contains(@id,'skip_back')]"
back_xpath2 = "(//*[contains(@id,'skip_back')])[2]"
forward_kmc = "div[class*='skipForward']"
amp_forward_xpath = "//div[contains(@id,'skip-forward')]"
amp_forward_xpath2 = "(//div[contains(@id,'skip-forward')])[2]"
forward_amp = "div[id*='skip-forward']"
forward_display=""
ad_banner = "div[class='akamai-ad-banner']"
ad_caption = 'div[class="ad-info-caption"]'
ad_bc = "div[class='videoAdUiPreSkipContainer']"
amp_back_xpath = "//div[contains(@id,'skip-back')]"
amp_back_xpath2 = "(//div[contains(@id,'skip-back')])[2]"
kmc_thumb_up_xpath = "//img[contains(@src,'like-kaltura.png')]"
kmc_thumb_down_xpath = "//img[contains(@src,'dislike-kaltura.png')]"
thumb_up_xpath = "//*[contains(@id,'thumbs_up')]"
thumb_up_xpath2 = "(//*[contains(@id,'thumbs_up')])[2]"
thumb_down_xpath = "//*[contains(@id,'thumbs_down')]"
thumb_down_xpath2 = "(//*[contains(@id,'thumbs_down')])[2]"
amp_thumb_up_xpath = "//*[contains(@id,'thumbs-up')]"
amp_thumb_down_xpath = "//*[contains(@id,'thumbs-down')]"
amp_thumb_up_xpath2 = "(//*[contains(@id,'thumbs-up')])[2]"
amp_thumb_down_xpath2 = "(//*[contains(@id,'thumbs-down')])[2]"
start_next_slate='div[id$="start-next-slate"]'
end_next_slate='div[id$="end-next-slate"]'
bc_mute="//div[@class='vjs-control-bar']/div[1]"
o_mute = "//button[contains(@class,'vjs-mute-control')]"
pause = "button[class='vjs-play-control vjs-control vjs-button vjs-playing']"
vdb_mute='//div[contains(@class,"volume-button")]'
play = 'div[class*="vjs-big-play-button"]'
play2 = 'div[class*="icon-play"]'
kmc_mute='//div[contains(@class,"comp volumeControl")]/button'
jw_mute='//div[contains(@class,"jw-icon jw-icon-tooltip jw-icon-volume")]'
tp_mute='//canvas[@class="IconUnmuted"]'
js_forward = "if(document.querySelector('[id*=skip_forward]')) document.querySelector('[id*=skip_forward]').click(); else if (document.querySelector('[id*=skip-forward]'))document.querySelector('[id*=skip-forward]').click(); else if (document.querySelector('[src*=\"brightcove/buttons/next.png\"]') != null) document.querySelector('[src*=\"brightcove/buttons/next.png\"]').click();"
js_forward2 = "if(document.querySelectorAll('[id*=skip_forward]')) document.querySelectorAll('[id*=skip_forward]')[1].click(); else if (document.querySelectorAll('[id*=skip-forward]')) document.querySelectorAll[1]('[id*=skip-forward]')[1].click(); else if (document.querySelectorAll('[src*=\"brightcove/buttons/next.png\"]') != null) document.querySelectorAll('[src*=\"brightcove/buttons/next.png\"]')[1].click();"
js_back = "if(document.querySelector('[id*=skip_back]')) document.querySelector('[id*=skip_back]').click(); else if(document.querySelector('[id*=skip-back]')) document.querySelector('[id*=skip-back]').click(); else if (document.querySelector('[src*=\"brightcove/buttons/prev.png\"]') != null) document.querySelector('[src*=\"brightcove/buttons/prev.png\"]').click();"
js_back2 = "if(document.querySelectorAll('[id*=skip_back]')) document.querySelectorAll('[id*=skip_back]')[1].click(); else if(document.querySelectorAll('[id*=skip-back]')) document.querySelectorAll('[id*=skip-back]')[1].click(); else if (document.querySelectorAll('[src*=\"brightcove/buttons/prev.png\"]') != null) document.querySelectorAll('[src*=\"brightcove/buttons/prev.png\"]')[1].click();"
js_thumb_down="if(document.querySelector('[id*=thumbs_down]') != null) document.querySelector('[id*=thumbs_down]').click(); else if(document.querySelector('[id*=thumbs-down]') != null) document.querySelector('[id*=thumbs-down]').click(); else if (document.querySelector('[src*=\"brightcove/buttons/dislike.png\"]') != null) document.querySelector('[src*=\"brightcove/buttons/dislike.png\"]').click();"
js_thumb_down2="if(document.querySelectorAll('[id*=thumbs_down]') != null) document.querySelectorAll('[id*=thumbs_down]')[1].click(); else if(document.querySelectorAll('[id*=thumbs-down]') != null) document.querySelectorAll('[id*=thumbs-down]')[1].click(); else if (document.querySelectorAll('[src*=\"brightcove/buttons/dislike.png\"]') != null) document.querySelectorAll('[src*=\"brightcove/buttons/dislike.png\"]')[1].click();"
js_thumb_up="if(document.querySelector('[id*=thumbs_up]') != null) document.querySelector('[id*=thumbs_up]').click(); else if(document.querySelector('[id*=thumbs-up]') != null) document.querySelector('[id*=thumbs-up]').click(); else if (document.querySelector('[src*=\"brightcove/buttons/like.png\"]') != null) document.querySelector('[src*=\"brightcove/buttons/like.png\"]').click();"
js_thumb_up2="if(document.querySelectorAll('[id*=thumbs_up]') != null) document.querySelectorAll('[id*=thumbs_up]')[1].click(); else if(document.querySelectorAll('[id*=thumbs-up]') != null) document.querySelectorAll('[id*=thumbs-up]')[1].click(); else if (document.querySelectorAll('[src*=\"brightcove/buttons/like.png\"]') != null) document.querySelectorAll('[src*=\"brightcove/buttons/like.png\"]')[1].click();"
js_player_type='return (function() { if (typeof bc != "undefined" && typeof bc.VERSION != "undefined") return "bc"; else if(typeof jwplayer != "undefined") return "jw"; else if(typeof kWidget != "undefined" || typeof KWidget != "undefined") return "kmc"; else if (typeof AKAMAI_MEDIA_PLAYER != "undefined" || typeof akamai != "undefined") return "amp"; else if (typeof vdb != "undefined" || typeof vidible != "undefined") return "vdb"; else if (typeof tpScriptPath != "undefined" || typeof tpk != "undefined") return "tp"; else if (typeof THEOplayer != "undefined" || typeof theoplayer != "undefined") return "oplayer"; else return "unknown"} )();'
js_bc_v= 'return (function() { if (typeof bc != "undefined" && typeof bc.VERSION != "undefined") return bc.VERSION;} )(); '
js_play = "if(document.querySelector(\"button[class*='play-button']\") != null) document.querySelector(\"button[class*='play-button']\").click(); else if (document.querySelector(\"a[class*='icon-play']\") != null) document.querySelector(\"a[class*='icon-play']\").click(); else if(typeof document.getElementsByClassName('vjs-play-control vjs-control vjs-button')[0] != 'undefined') document.getElementsByClassName('vjs-play-control vjs-control vjs-button')[0].click();"
js_play2 = "if(document.querySelectorAll(\"button[class*='play-button']\") != null) document.querySelectorAll(\"button[class*='play-button']\")[1].click(); else if (document.querySelectorAll(\"a[class*='icon-play']\") != null) document.querySelectorAll(\"a[class*='icon-play']\")[1].click(); else if(typeof document.querySelectorAll('[class=\"vjs-play-control vjs-control vjs-button\"]') != 'undefined') document.querySelectorAll('[class=\"vjs-play-control vjs-control vjs-button\"]')[1].click();"
js_playlist_len = 'return (function() { if(typeof iris != "undefined" && typeof iris.getPlaylist != "undefined") return iris.getPlaylist().length; else if (typeof IrisEngine != "undefined" && typeof IrisEngine.getPlaylist != "undefined") return IrisEngine.getPlaylist().length; else if (typeof iris1 != "undefined" && typeof iris1.getPlaylist != "undefined") return iris1.getPlaylist().length; else if (typeof iris_player != "undefined" && typeof iris_player.getPlaylist != "undefined") return iris_player.getPlaylist().length; else if (typeof iris_player != "undefined" && typeof iris_player.getPlaylist != "undefined") return iris_player.getPlaylist().length;} )();'
js_getIndex = 'return (function() { if(typeof iris != "undefined" && typeof iris.getCurrentIndex != "undefined") return iris.getCurrentIndex(); else if (typeof IrisEngine != "undefined" && typeof IrisEngine.getCurrentIndex != "undefined") return IrisEngine.getCurrentIndex(); else if (typeof iris1 != "undefined" && typeof iris1.getCurrentIndex != "undefined") return iris1.getCurrentIndex(); else if (typeof iris_player != "undefined" && typeof iris_player.getCurrentIndex != "undefined") return iris_player.getCurrentIndex(); else if (typeof iris_player != "undefined" && typeof iris_player.currentIndex != "undefined") return iris_player.currentIndex;} )();'
js_get_asset_amp = 'return (function() { if(typeof iris != "akami" && typeof akamai.streamURL != "undefined") return akamai.streamURL;} )();'
js_get_video_src= 'return (function() { try{ if(typeof document.getElementsByTagName("video")[0] != "undefined" && document.getElementsByTagName("video")[0].getAttribute("src") != null) return document.getElementsByTagName("video")[0].getAttribute("src"); else if(typeof document.getElementsByTagName("video")[1] != "undefined" && document.getElementsByTagName("video")[1].getAttribute("src") != null) return document.getElementsByTagName("video")[1].getAttribute("src"); else if(document.getElementsByTagName("iframe")[0] != "undefined" && document.getElementsByTagName("iframe")[0].contentWindow.document.getElementsByTagName("video")[0] != "undefined") return document.getElementsByTagName("iframe")[0].contentWindow.document.getElementsByTagName("video")[0].getAttribute("src"); else if(document.getElementsByTagName("iframe")[1] != "undefined" && document.getElementsByTagName("iframe")[1].contentWindow.document.getElementsByTagName("video")[0] != "undefined") return document.getElementsByTagName("iframe")[1].contentWindow.document.getElementsByTagName("video")[0].getAttribute("src")} catch(e){} } )();'
js_get_iframe= 'return (function() {try{ var irisqa_iframes = document.getElementsByTagName("iframe"); for (var x=0; x<irisqa_iframes.length;x++) { irisqa_iframe= irisqa_iframes[x].contentDocument || irisqa_iframes[x].contentWindow.document; if(irisqa_iframes[x].getAttribute("id")!= null && irisqa_iframes[x].getAttribute("id").toLowerCase().indexOf("adframe") >=0) {continue} else if(irisqa_iframe && irisqa_iframe.body.innerHTML && irisqa_iframe.body.innerHTML.match(/AolHtml5Player/)) return x+1;} }catch(e){} } )();'

def set_player(player,version):
	global ver,iframe,mute,iframe1
	if player=="bc":
		iframe=""
		mute=bc_mute
		if version and version != "" and int(version.split(".")[0]) >= 6:
			mute=mute+"/button"
	elif player== "jw":
		iframe=""
		mute=jw_mute
	elif player== "kmc":
		iframe=""
		mute=kmc_mute
	elif player== "vdb":
		mute=vdb_mute
		iframe=""
	elif player== "tp":
		iframe=""
		mute=tp_mute
	elif player== "amp":
		iframe=""
		mute=""
	elif player=="oplayer":
		iframe=""
		mute=o_mute
	elif player == "unknown":
		print "Unknown player type/platform"
	if version and version != "":
		print "Player version: " + version

class Headless():
	def start(self):
		global headless
		self.display = Display(visible=0, size=(1024, 768))
		self.display.start()
		return self.display


class Setup():   
    def browser(self,proxy,ssl_proxy):
    	global browser,url,js_player_type
    	prox = Proxy()
    	prox.proxy_type = ProxyType.MANUAL
    	prox.http_proxy = proxy
    	prox.socks_proxy = proxy
    	prox.ssl_proxy = ssl_proxy
    	prox.autodetect = False
    	if browser=="chrome":
    		chrome_options = webdriver.ChromeOptions()
    		chrome_options.add_argument('--proxy-server==http://%s' % proxy)
    		chrome_options.add_argument('--ignore-certificate-errors')
    		self.driver = webdriver.Chrome(chrome_options=chrome_options)
    	elif browser=="safari":
    		caps = webdriver.SafariOptions()
    		caps.add_argument('--proxy-server==http://%s' % proxy)
    		self.driver = webdriver.Safari(chrome_options=caps)
    	elif browser=="edge":
    		caps = webdriver.DesiredCapabilities.EDGE
    		prox.add_to_capabilities(caps)
    		self.driver  = webdriver.Edge(capabilities=caps)
    	elif browser=="ie":
            caps = webdriver.DesiredCapabilities.INTERNETEXPLORER
            caps['acceptInsecureCerts'] = True
            prox.add_to_capabilities(caps)
            self.driver = webdriver.Ie(capabilities=caps)
        else:
            self.profile  = webdriver.FirefoxProfile()
            self.profile.set_proxy(prox)
            self.profile.accept_untrusted_certs = True
            self.driver = webdriver.Firefox(firefox_profile=self.profile)
    	return self.driver

    def player(self,url):
    	global iframe,mute,player,js_bc_v,js_player_type,js_play,multiplayer,play,expected_watch, pause,ilink,timeout,forward_xpath,slow_loading
    	self.driver.implicitly_wait(3)
    	print url
    	if page_load_timeout:
            self.driver.set_page_load_timeout(timeout)
            self.driver.get(blank_html)
            self.driver.execute_script('location.href = "'+ url + '"; ')
            print "waiting for page to load"
            try:
                alert = self.driver.switch_to_alert()
                alert.accept()
            except:
                print "no alert"
            element = WebDriverWait(self.driver, timeout).until(
                wait_for_page_load()
                )
            print "page should be loaded"
            time.sleep(5)
    	else: 
    		self.driver.get(url)
    		try:
    			alert = self.driver.switch_to_alert()
    			alert.accept()
    		except:
    			print "no alert"
    	player = self.driver.execute_script(js_player_type)
        if player == "unknown" and page_load_timeout:
            time.sleep(5)
            player = self.driver.execute_script(js_player_type)
        v= self.driver.execute_script(js_bc_v)
    	set_player(player,v)
    	print "Player type: " + player
    	iframe_list = self.driver.find_elements_by_css_selector(kmc_iframe)
    	if len(iframe_list) >0:
    		self.driver.switch_to.frame(self.driver.find_element_by_css_selector(kmc_iframe))
    		print "Switching to kmc iframe"
    	else:
    		iframe_num = self.driver.execute_script(js_get_iframe)
    		if iframe_num and iframe_num != "":
    			iframe = "(//iframe)[" + str(iframe_num) + "]"
    			self.driver.switch_to.frame(self.driver.find_element_by_xpath(iframe))
    			print "Switching to iframe: " + iframe
    	playing_list = self.driver.find_elements_by_css_selector(pause)
    	if len(playing_list) >= 2:
    		self.driver.execute_script("arguments[0].click();", playing_list[1])
    		print "Pausing second player, we recommend auto-play be disabled thru Brightcove since extra API calls will be introduced by second player causing tests to fail"
    	self.driver.execute_script(js_play)
        if multiplayer == True:
            self.driver.execute_script(js_play2)
    	p_list = self.driver.find_elements_by_css_selector(play2)
    	if len(p_list) > 0 and p_list[0].is_displayed():
    		p_list[0].click()
    	if mute != "":
    		mute_list = self.driver.find_elements_by_xpath(mute)
    		if len(mute_list) > 0:
    			element = self.driver.find_element_by_xpath(mute)
    			self.driver.execute_script("arguments[0].click();", element)
    		if len(mute_list) >=2:
    			self.driver.execute_script("arguments[0].click();", mute_list[1])
    	# if player == "vdb":
    	# 	self.driver.switch_to.default_content()
    	if len(self.driver.find_elements_by_css_selector(play)) >= 2:
    		multiplayer = False
    	if multiplayer == True:
    		expected_watch = expected_watch * 2
    	self.driver.implicitly_wait(11)
    	#wait for initial add to finish playing
    	return self.driver

class Player(object):
    def __init__(self,driver):
        self.driver = driver

    def is_element_present(self,locator):
        try:
            self.driver.find_element_by_css_selector(locator)
        except NoSuchElementException:
            return False
        return True

    def get_style_attr(self,locator):
        try:
            t = False
            e = self.driver.find_element_by_css_selector(locator)
            s = e.get_attribute("style")
            if 'display' in s:
                t=s.split(':')[1] 
        except NoSuchElementException:
            return False
        return t

    def click_forward(self):
		global player, forward_xpath,js_forward, amp_forward_xpath
		el_list = self.driver.find_elements_by_xpath(amp_forward_xpath)
		if len(el_list) > 0:
			forward_loc = amp_forward_xpath
		else:
			forward_loc = forward_xpath
		element = WebDriverWait(self.driver, 15).until(
			EC.presence_of_element_located((By.XPATH, forward_loc)))
		time.sleep(2)
		self.driver.execute_script(js_forward)

    def click_forward_player2(self):
        global player, forward_xpath,js_forward, amp_forward_xpath
        el_list = self.driver.find_elements_by_xpath(amp_forward_xpath)
        if len(el_list) > 0:
            forward_loc = amp_forward_xpath2
        else:
            forward_loc = forward_xpath2
        element = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, forward_loc)))
        time.sleep(2)
        self.driver.execute_script(js_forward2)

    def wait_for_forward(self):
        global forward_xpath,amp_forward_xpath, forward_kmc,forward_amp,timeout,forward_display, forward
        print "waiting for skip forward to be present"
        if self.is_element_present(forward_kmc) and self.get_style_attr(forward_kmc) and "none" in self.get_style_attr(forward_kmc):
            forward_display = forward_kmc
            WebDriverWait(self.driver, preroll_timeout).until(
                    wait_for_forward_display()
                    )
        elif self.is_element_present(forward_amp) and self.get_style_attr(forward_amp) and "none" in self.get_style_attr(forward_amp):
            forward_display = forward_amp
            WebDriverWait(self.driver, preroll_timeout).until(
                wait_for_forward_display()
                )
        elif self.is_element_present(forward) and self.get_style_attr(forward) and "none" in self.get_style_attr(forward):
            forward_display = forward
            WebDriverWait(self.driver, preroll_timeout).until(
                wait_for_forward_display()
                )
        else:
            el_list = self.driver.find_elements_by_xpath(amp_forward_xpath)
            if len(el_list) > 0:
                forward_loc = amp_forward_xpath
            else:
                forward_loc = forward_xpath
            element = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, forward_loc))
                )

    def wait_for_ad(self):
        global timeout, ad_bc, ad_banner, ad_caption, preroll_ads
        if preroll_ads:
            print "checking if ad displayed"
            self.driver.implicitly_wait(1)
            if self.is_element_present(ad_banner):
                element = WebDriverWait(self.driver, timeout).until_not(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ad_banner))
                    )
            elif self.is_element_present(ad_caption):
                element = WebDriverWait(self.driver, timeout).until_not(
                    EC.visibility_of_element_located((PlayerLocators.VDB_AD_CAPTION))
                    )
            elif self.is_element_present(ad_bc):
                element = WebDriverWait(self.driver, timeout).until_not(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,ad_bc))
                    )
            self.driver.implicitly_wait(11)

    def click_back(self):
		global player, js_back, back_xpath, amp_back_xpath
		el_list = self.driver.find_elements_by_xpath(amp_back_xpath)
		if len(el_list) > 0:
			back_loc = amp_back_xpath
		else:
			back_loc = back_xpath
		element = WebDriverWait(self.driver, 15).until(
			EC.presence_of_element_located((By.XPATH, back_loc)))
		self.driver.execute_script(js_back)

    def click_back_player2(self):
        global player, js_back, back_xpath, amp_back_xpath
        el_list = self.driver.find_elements_by_xpath(amp_back_xpath)
        if len(el_list) > 0:
            back_loc = amp_back_xpath2
        else:
            back_loc = back_xpath2
        element = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, back_loc)))
        self.driver.execute_script(js_back2)

    def click_thumb_up(self):
		global player, js_thumb_up,thumb_up_xpath,amp_thumb_up_xpath
		el_list = self.driver.find_elements_by_xpath(amp_thumb_up_xpath)
		if len(el_list) > 0:
			thumb_up = amp_thumb_up_xpath
		else:
			thumb_up = thumb_up_xpath
		element = WebDriverWait(self.driver, 15).until(
				EC.presence_of_element_located((By.XPATH, thumb_up))
			)
		self.driver.execute_script(js_thumb_up)

    def click_thumb_up_player2(self):
        global player, js_thumb_up,thumb_up_xpath,amp_thumb_up_xpath
        el_list = self.driver.find_elements_by_xpath(amp_thumb_up_xpath)
        if len(el_list) > 0:
            thumb_up = amp_thumb_up_xpath2
        else:
            thumb_up = thumb_up_xpath2
        element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, thumb_up))
            )
        self.driver.execute_script(js_thumb_up2)

    def click_thumb_down(self):
		global player, js_thumb_down,thumb_down_xpath,amp_thumb_down_xpath
		el_list = self.driver.find_elements_by_xpath(amp_thumb_down_xpath)
		if len(el_list) > 0:
			thumb_down = amp_thumb_down_xpath
		else:
			thumb_down = thumb_down_xpath
		element = WebDriverWait(self.driver, 15).until(
				EC.presence_of_element_located((By.XPATH, thumb_down))
			)
		self.driver.execute_script(js_thumb_down)

    def click_thumb_down_player2(self):
        global player, js_thumb_down,thumb_down_xpath,amp_thumb_down_xpath
        el_list = self.driver.find_elements_by_xpath(amp_thumb_down_xpath)
        if len(el_list) > 0:
            thumb_down = amp_thumb_down_xpath
        else:
            thumb_down = thumb_down_xpath
        element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, thumb_down))
            )
        self.driver.execute_script(js_thumb_down2)

    def click_end_next_slate(self):
		global end_next_slate, max_timeout
		element = WebDriverWait(self.driver, max_timeout).until(
				EC.element_to_be_clickable((By.CSS_SELECTOR, end_next_slate))
			)
		element.click()
		print "Clicked end next slate"

    def get_end_next_slate(self):
		global end_next_slate, max_timeout
		element = WebDriverWait(self.driver, max_timeout).until(
				EC.element_to_be_clickable((By.CSS_SELECTOR, end_next_slate))
			)
		temp = element.text 
		element.click()
		print "Clicked end next slate"
		return temp

    def click_start_next_slate(self):
		global start_next_slate
		element = WebDriverWait(self.driver, 15).until(
				EC.element_to_be_clickable((By.CSS_SELECTOR, start_next_slate))
			)
		element.click()
		print "Clicked start next slate"

    def get_start_next_slate(self):
		global start_next_slate
		element = WebDriverWait(self.driver, 15).until(
				EC.element_to_be_clickable((By.CSS_SELECTOR, start_next_slate))
			)
		temp = element.text
		element.click()
		print "Clicked start next slate"
		return temp

    def get_first_video(self):
		global video1
		video1 = self.driver.execute_script(js_get_video_src)
		if video1:
			print "Video: " + video1
			return True
		else:
			return False

class wait_for_index_to_change():
	def __call__(self, driver):
		global js_getIndex
		try:
			index = driver.execute_script(js_getIndex)
			return int(index) > 0
		except TimeoutException:
			print "Verify max_timeout is setup correctly for length of first video"
			return 0

class wait_for_video_to_change():
	def __call__(self, driver):
		global video1
		try:
			video = driver.execute_script(js_get_video_src)
			return video1 != video
		except TimeoutException:
			print "Verify max_timeout is setup correctly for length of first video"
			return 0

class wait_for_page_load():
	def __call__(self, driver):
		try:
			page_state = driver.execute_script('return document.readyState;') 
			return page_state == 'complete'
		except TimeoutException:
			print "Verify max_timeout is setup correctly"
			return False

class wait_for_forward_display():
    def __call__(self, driver):
        try:
            t= "none"
            e = driver.find_element_by_css_selector(forward_display)
            s = e.get_attribute("style")
            if 'display' in s:
                t=s.split(':')[1]
            return "block" in t
        except TimeoutException:
            print "Verify max_timeout is setup correctly"
            return False

class wait_for_first_video():
	def __call__(self, driver):
		try:
			temp = driver.execute_script(js_get_video_src)
			if temp and temp != "":
				video = True
				print "Video: " + temp
			else:
				video = False
			return video == True
		except TimeoutException:
			print "Verify max_timeout is setup correctly for length of first video"
			return False

def check_browser_errors(driver):
    """
    Checks browser for errors, returns a list of errors
    :param driver:
    :return:
    """
    try:
    	browserlogs = driver.get_log('browser')
    except (ValueError, WebDriverException) as e:
        # Some browsers does not support getting logs
        print "Could not get browser logs for driver due to exception: " + str(e)
        #LOGGER.debug("Could not get browser logs for driver %s due to exception: %s", driver, e)
        return []

    errors = []
    for entry in browserlogs:
    	if entry['level'] == 'SEVERE':
    		errors.append(entry)
    print str(errors)

def get_screenshot_filename():
    global dir
    filename = dir+ "/reports/screenshot" + "-" + str(int(time.time())) + ".png"
    print "\nScreenshot: " + filename
    return filename

def get_update_calls(tempJson):
	for index,x in enumerate(tempJson):
		print "\nUpdate Call: " + str(index)
		print "Platform id: " + x.get("platform_id","")
		if x.get("title"):
			print "Asset title: " + x.get("title","")
		if x.get("behavior[percentage_watched]"):
			print "behavior[percentage_watched]: " + x.get("behavior[percentage_watched]","")
		if x.get("behavior[next]"):
			print "behavior[next]: " + x.get("behavior[next]","")
		if x.get("behavior[play]"):
			print "behavior[play]: " + x.get("behavior[play]","")
		if x.get("behavior[next_auto]"):
			print "behavior[next_auto]: " + x.get("behavior[next_auto]","")
		if x.get("behavior[video_complete]"):
			print "behavior[video_complete]: " + x.get("behavior[video_complete]","")
		if x.get("behavior[thumbs_down]"):
			print "behavior[thumbs_down]: " + x.get("behavior[thumbs_down]","")
		if x.get("behavior[thumbs_up]"):
			print "behavior[thumbs_up]: " + x.get("behavior[thumbs_up]","")
		if x.get("behavior[start_next_slate]"):
			print "behavior[start_next_slate]: " + x.get("behavior[start_next_slate]","")
		if x.get("behavior[end_next_slate]"):
			print "behavior[end_next_slate]: " + x.get("behavior[end_next_slate]","")
		if x.get("experience"):
			print "experience: " + x.get("experience","")

def check_iris_files(iris_files):
	combined_irisfiles = '\t'.join(iris_files)
	print "\nIRIS FILES REQUESTED" 
	for i in iris_files:
		print i
	if '.css' not in combined_irisfiles:
		print "No Iris CSS was loaded (not added to HTML source code)\n"
	return combined_irisfiles

def check_platform_id(tempJson):
	r=0;
	for index,x in enumerate(tempJson):
		if not x.get("platform_id"):
			r+=1;
	return r

def update_maxi(num):
	global campaign_tracking
	if campaign_tracking:
		num = num +2
	return num

def count_actions(tempJson, behavior):
	r=0;
	for x in tempJson:
		if x.get(behavior):
			r+=1;
	return r

def check_behavior(tempJson, behavior):
	for x in tempJson:
		if x.get(behavior):
			return x.get(behavior)

def get_percentage_watched(tempJson):
	watched = []
	for x in tempJson:
		if x.get("behavior[percentage_watched]") and x.get("behavior[percentage_watched]") != "1.00":
			p = x.get("behavior[percentage_watched]").encode('ascii', 'ignore')
			if int(p.replace("0.","")) in range (20,30):
				watched.append(p)
			elif int(p.replace("0.","")) in range (40,60):
				watched.append(p)
			elif int(p.replace("0.","")) in range (70,80):
				watched.append(p)
	return watched

def get_json(tempJson):
    t = tempJson[0][:len(tempJson[0])-1]
    t = t[t.index("{"):]
    j=json.loads(t)
    return j


def get_playlist(tempJson):
	djson = get_json(tempJson)
	n=djson['next']
	return n

def get_playlist_length(tempJson):
    djson = get_json(tempJson)
    return len(djson["next"])

def check_for_dup_recs(playlist, tempJson):
    dup = False
    for x in tempJson:
        djson = get_json(tempJson)
        n=djson['next']
        if playlist == n:
            dup = True
    return dup

def check_single_response(tempJson):
    tsring = json.dumps(tempJson[0])
    if "Sclera " in tsring:
        print "\nALERT DevOps, API error: " + tsring
    elif '"message":' in tsring:
            print "API error: " + tsring
    else:
        djson = get_json(tempJson)
        s=djson['success']
        if 'default_recs' in tsring and djson['default_recs'] == True:
            print "\nWARN: possible rec issue, default_recs:true"
        return s

def check_response(tempJson):
    n=0
    for x in tempJson:
        tsring = json.dumps(tempJson)
        if "Sclera " in tsring:
            print "\nALERT DevOps, API error: " + tsring
        elif '"message":' in tsring:
            print "API error: " + tsring
        else:
            djson = get_json(tempJson)
            s=djson['success']
            if s != True:
                n=n+1
            if 'default_recs' in tsring and djson['default_recs'] == True:
                print "\nWARN: possible rec issue, default_recs:true"
    return n
    
def get_platform_ids(tempJson):
	djson = get_json(tempJson)
	playlist=djson['next']
	platform_ids = []
	for p in playlist:
		i = p.get("platform_id","")
		platform_ids.append(i)
	return platform_ids
	
def set_watch_call_params(tempJson):
	global campaign_tracking, end_up_next_text, start_up_next_text
	for index,x in enumerate(tempJson):
		if x.get("start_up_next_text"):
			start_up_next_text = x.get("start_up_next_text","")
		if x.get("end_up_next_text"):
			end_up_next_text = x.get("end_up_next_text","")
		if x.get("campaign_tracking","") == "true":
			campaign_tracking = True
		else:
			campaign_tracking = False
		if x.get("start_up_next","") == "true":
			start_up_next = True
		else:
			start_up_next = False
		if x.get("end_up_next","") == "true":
			end_up_next = True
		else:
			end_up_next = False

def get_watch_calls(tempJson):
	global campaign_tracking, end_up_next_text, start_up_next_text
	for index,x in enumerate(tempJson):
		print "\nWatch Call: " + str(index)
		print "Platform id: " + x.get("platform_id","")
		print "Client token: " + x.get("client_token","")
        if x.get("disable_mobile_upnext"):
            print "disable_mobile_upnext: " + x.get("disable_mobile_upnext","")
        else:
            print "(upnext is disabled for mobile, parameter was not passed)"
        if x.get("start_up_next"):
            print "start_up_next: " + x.get("start_up_next","")
        if x.get("start_up_next_text"):
            print "Start up next text: " + x.get("start_up_next_text","")
        if x.get("start_up_next_text"):
            start_up_next_text = x.get("start_up_next_text","")
        if x.get("end_up_next_text"):
            end_up_next_text = x.get("end_up_next_text","")
        if x.get("end_up_next"):
            print "end_up_next: " + x.get("end_up_next","")
        if x.get("end_up_next_text"):
            print "End up next text: " + x.get("end_up_next_text","")
        if x.get("campaign_tracking"):
            print "Campaign tracking: " + x.get("campaign_tracking","")
        if x.get("experience"):
            print "experience: " + x.get("experience","")
        if x.get("campaign_tracking","") == "true":
            campaign_tracking = True
        else:
            campaign_tracking = False

def get_next_calls(tempJson):
	global campaign_tracking
	for index,x in enumerate(tempJson):
		print "\nNext Call: " + str(index)
		print "Platform id: " + x.get("platform_id","")
		print "Client token: " + x.get("client_token","")
		if x.get("start_up_next_text"):
			print "Start up next text: " + x.get("start_up_next_text","")
		if x.get("end_up_next_text"):
			print "End up next text: " + x.get("end_up_next_text","")
		print "Campaign tracking: " + x.get("campaign_tracking","")
		if x.get("experience"):
			print "experience: " + x.get("experience","")

def total_calls(watch_calls,update_calls,next_calls):
	print "\nTotal watch calls " + str(len(watch_calls))
	print "Total update calls " + str(len(update_calls))
	print "Total next calls " + str(len(next_calls))
