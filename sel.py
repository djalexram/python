import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from locators import PlayerLocators
import time
import json
import sys


player = 2

#Other variables
arg_url = ""
iris_path = 's3.amazonaws.com/iris-playground'
iris_js = 'iris.adaptive.js'
iris_api = 'api.iris.tv'
iris_watch = 'iris.tv/watch'
iris_update = 'iris.tv/update'
iris_next = 'iris.tv/next'
bc_play="(//button[@class='vjs-big-play-button'])[1]"
chrome_termsID="terms_accept"
player_type='bc'
iframe=""
mute=""
ver=""
video1=""
frame_kmc="kaltura_player_ifp"
kmc_iframe = "iframe[class*='EmbedKalturaIframe']"
the_platform_iframe = "//iframe[contains(@src,'player.theplatform.com')]"
campaign_tracking=False
start_up_next_text=""
end_up_next_text=""
start_up_next=True
end_up_next=True
player_error = "Setup Timeout Error: Setup took longer than 30 seconds to complete"
appium_url = 'http://s3.amazonaws.com/iris-playground/cosmos/test_pages/brightcovenextgen.html'
browsermob_options = '{"captureHeaders": True, "captureContent": True, "captureBinaryContent": False}'
forward_xpath = "//*[contains(@id,'skip_forward')]"
forward_xpath2 = "(//*[contains(@id,'skip_forward')])["+str(player)+"]"
forward = "div[class*='skip_forward']"
back_xpath = "//*[contains(@id,'skip_back')]"
back_xpath2 = "(//*[contains(@id,'skip_back')])["+str(player)+"]"
forward_kmc = "div[class*='skipForward']"
amp_forward_xpath = "//div[contains(@id,'skip-forward')]"
amp_forward_xpath2 = "(//div[contains(@id,'skip-forward')])["+str(player)+"]"
platform_forward = "//div[@class='tpNext']/canvas"
platform_back = "//div[@class='tpPrevious']/canvas"
forward_amp = "div[id*='skip-forward']"
forward_display=""
ad_banner = "div[class='akamai-ad-banner']"
ad_caption = 'div[class="ad-info-caption"]'
ad_bc = "div[class='videoAdUiPreSkipContainer']"
ad_plat = "div[contains(text(),'Your video will resume in')]"
amp_back_xpath = "//div[contains(@id,'skip-back')]"
amp_back_xpath2 = "(//div[contains(@id,'skip-back')])["+str(player)+"]"
kmc_thumb_up_xpath = "//img[contains(@src,'like-kaltura.png')]"
kmc_thumb_down_xpath = "//img[contains(@src,'dislike-kaltura.png')]"
thumb_up_xpath = "//*[contains(@id,'thumbs_up')]"
thumb_up_xpath2 = "(//*[contains(@id,'thumbs_up')])["+str(player)+"]"
thumb_down_xpath = "//*[contains(@id,'thumbs_down')]"
thumb_down_xpath2 = "(//*[contains(@id,'thumbs_down')])["+str(player)+"]"
amp_thumb_up_xpath = "//*[contains(@id,'thumbs-up')]"
amp_thumb_down_xpath = "//*[contains(@id,'thumbs-down')]"
amp_thumb_up_xpath2 = "(//*[contains(@id,'thumbs-up')])["+str(player)+"]"
amp_thumb_down_xpath2 = "(//*[contains(@id,'thumbs-down')])["+str(player)+"]"
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
js_forward = "if(document.querySelector('[id*=skip_forward]')) document.querySelector('[id*=skip_forward]').click(); else if (document.querySelector('[class=tpNext] > canvas')) document.querySelector('[class=tpNext] > canvas').click(); else if (document.querySelector('[id*=skip-forward]'))document.querySelector('[id*=skip-forward]').click(); else if (document.querySelector('[src*=\"brightcove/buttons/next.png\"]') != null) document.querySelector('[src*=\"brightcove/buttons/next.png\"]').click();"
js_forward2 = "if(document.querySelectorAll('[id*=skip_forward]')) document.querySelectorAll('[id*=skip_forward]')["+str(player-1)+"].click(); else if (document.querySelectorAll('[id*=skip-forward]')) document.querySelectorAll('[id*=skip-forward]')["+str(player-1)+"].click(); else if (document.querySelectorAll('[src*=\"brightcove/buttons/next.png\"]') != null) document.querySelectorAll('[src*=\"brightcove/buttons/next.png\"]')["+str(player-1)+"].click();"
js_back = "if(document.querySelector('[id*=skip_back]')) document.querySelector('[id*=skip_back]').click(); else if (document.querySelector('[class=tpPrevious] > canvas')) document.querySelector('[class=tpPrevious] > canvas').click(); else if(document.querySelector('[id*=skip-back]')) document.querySelector('[id*=skip-back]').click(); else if (document.querySelector('[src*=\"brightcove/buttons/prev.png\"]') != null) document.querySelector('[src*=\"brightcove/buttons/prev.png\"]').click();"
js_back2 = "if(document.querySelectorAll('[id*=skip_back]')) document.querySelectorAll('[id*=skip_back]')["+str(player-1)+"].click(); else if(document.querySelectorAll('[id*=skip-back]')) document.querySelectorAll('[id*=skip-back]')["+str(player-1)+"].click(); else if (document.querySelectorAll('[src*=\"brightcove/buttons/prev.png\"]') != null) document.querySelectorAll('[src*=\"brightcove/buttons/prev.png\"]')["+str(player-1)+"].click();"
js_thumb_down="if(document.querySelector('[id*=thumbs_down]') != null) document.querySelector('[id*=thumbs_down]').click(); else if(document.querySelector('[id*=thumbs-down]') != null) document.querySelector('[id*=thumbs-down]').click(); else if (document.querySelector('[src*=\"brightcove/buttons/dislike.png\"]') != null) document.querySelector('[src*=\"brightcove/buttons/dislike.png\"]').click();"
js_thumb_down2="if(document.querySelectorAll('[id*=thumbs_down]') != null) document.querySelectorAll('[id*=thumbs_down]')["+str(player-1)+"].click(); else if(document.querySelectorAll('[id*=thumbs-down]') != null) document.querySelectorAll('[id*=thumbs-down]')[1].click(); else if (document.querySelectorAll('[src*=\"brightcove/buttons/dislike.png\"]') != null) document.querySelectorAll('[src*=\"brightcove/buttons/dislike.png\"]')["+str(player-1)+"].click();"
js_thumb_up="if(document.querySelector('[id*=thumbs_up]') != null) document.querySelector('[id*=thumbs_up]').click(); else if(document.querySelector('[id*=thumbs-up]') != null) document.querySelector('[id*=thumbs-up]').click(); else if (document.querySelector('[src*=\"brightcove/buttons/like.png\"]') != null) document.querySelector('[src*=\"brightcove/buttons/like.png\"]').click();"
js_thumb_up2="if(document.querySelectorAll('[id*=thumbs_up]') != null) document.querySelectorAll('[id*=thumbs_up]')["+str(player-1)+"].click(); else if(document.querySelectorAll('[id*=thumbs-up]') != null) document.querySelectorAll('[id*=thumbs-up]')["+str(player-1)+"].click(); else if (document.querySelectorAll('[src*=\"brightcove/buttons/like.png\"]') != null) document.querySelectorAll('[src*=\"brightcove/buttons/like.png\"]')["+str(player-1)+"].click();"
js_player_type='return (function() { if (typeof bc != "undefined" && typeof bc.VERSION != "undefined") return "bc"; else if(document.body.innerHTML.indexOf("theplatform") >0) return "thePlatform"; else if(typeof jwplayer != "undefined") return "jw"; else if(typeof kWidget != "undefined" || typeof KWidget != "undefined") return "kmc"; else if (typeof AKAMAI_MEDIA_PLAYER != "undefined" || typeof akamai != "undefined") return "amp"; else if (typeof vdb != "undefined" || typeof vidible != "undefined") return "vdb"; else if (typeof tpScriptPath != "undefined" || typeof tpk != "undefined") return "tp"; else if (typeof THEOplayer != "undefined" || typeof theoplayer != "undefined") return "oplayer"; else return "unknown"} )();'
js_bc_v= 'return (function() { if (typeof bc != "undefined" && typeof bc.VERSION != "undefined") return bc.VERSION;} )(); '
js_play = "if(document.querySelector('[class*=play-button]') != null) document.querySelector('[class*=play-button]').click(); else if (document.querySelector('[class*=play-icon]') != null) document.querySelector('[class*=play-icon]').click(); else if (document.querySelector('[id*=playButtonHolder]') != null) document.querySelector('[id*=playButtonHolder > canvas]').click(); else if (document.querySelector('[class*=icon-play]') != null) document.querySelector('[class*=icon-play]').click(); else if(typeof document.getElementsByClassName('vjs-play-control vjs-control vjs-button')[0] != 'undefined') document.getElementsByClassName('vjs-play-control vjs-control vjs-button')[0].click();"
js_play2 = "if(document.querySelectorAll('[class*=play-button]') != null) document.querySelectorAll('[class*=play-button]')["+str(player-1)+"].click(); else if (document.querySelectorAll('[class*=play-icon]') != null) document.querySelectorAll('[class*=play-icon]')["+str(player-1)+"].click(); else if (document.querySelectorAll('[class*=icon-play]') != null) document.querySelectorAll('[class*=icon-play]')["+str(player-1)+"].click(); else if(typeof document.querySelectorAll('[class=\"vjs-play-control vjs-control vjs-button\"]') != 'undefined') document.querySelectorAll('[class=\"vjs-play-control vjs-control vjs-button\"]')["+str(player-1)+"].click();"
js_playlist_len = 'return (function() { if(typeof iris != "undefined" && typeof iris.getPlaylist != "undefined") return iris.getPlaylist().length; else if (typeof IrisEngine != "undefined" && typeof IrisEngine.getPlaylist != "undefined") return IrisEngine.getPlaylist().length; else if (typeof iris1 != "undefined" && typeof iris1.getPlaylist != "undefined") return iris1.getPlaylist().length; else if (typeof iris_player != "undefined" && typeof iris_player.getPlaylist != "undefined") return iris_player.getPlaylist().length; else if (typeof iris_player != "undefined" && typeof iris_player.getPlaylist != "undefined") return iris_player.getPlaylist().length;} )();'
js_getIndex = 'return (function() { if(typeof iris != "undefined" && typeof iris.getCurrentIndex != "undefined") return iris.getCurrentIndex(); else if (typeof IrisEngine != "undefined" && typeof IrisEngine.getCurrentIndex != "undefined") return IrisEngine.getCurrentIndex(); else if (typeof iris1 != "undefined" && typeof iris1.getCurrentIndex != "undefined") return iris1.getCurrentIndex(); else if (typeof iris_player != "undefined" && typeof iris_player.getCurrentIndex != "undefined") return iris_player.getCurrentIndex(); else if (typeof iris_player != "undefined" && typeof iris_player.currentIndex != "undefined") return iris_player.currentIndex;} )();'
js_get_asset_amp = 'return (function() { if(typeof iris != "akami" && typeof akamai.streamURL != "undefined") return akamai.streamURL;} )();'
js_get_video_src= 'return (function() { try{ if(typeof document.getElementsByTagName("video")[0] != "undefined" && document.getElementsByTagName("video")[0].getAttribute("src") != null) return document.getElementsByTagName("video")[0].getAttribute("src"); else if(typeof document.getElementsByTagName("video")[1] != "undefined" && document.getElementsByTagName("video")[1].getAttribute("src") != null) return document.getElementsByTagName("video")[1].getAttribute("src"); else if(document.getElementsByTagName("iframe")[0] != "undefined" && document.getElementsByTagName("iframe")[0].contentWindow.document.getElementsByTagName("video")[0] != "undefined") return document.getElementsByTagName("iframe")[0].contentWindow.document.getElementsByTagName("video")[0].getAttribute("src"); else if(document.getElementsByTagName("iframe")[1] != "undefined" && document.getElementsByTagName("iframe")[1].contentWindow.document.getElementsByTagName("video")[0] != "undefined") return document.getElementsByTagName("iframe")[1].contentWindow.document.getElementsByTagName("video")[0].getAttribute("src")} catch(e){} } )();'
js_get_iframe= 'return (function() {try{ var irisqa_iframes = document.getElementsByTagName("iframe"); for (var x=0; x<irisqa_iframes.length;x++) { if(irisqa_iframes[x].src && irisqa_iframes[x].src == "") irisqa_iframe= irisqa_iframes[x].contentDocument || irisqa_iframes[x].contentWindow.document; if(irisqa_iframes[x].getAttribute("id")!= null && irisqa_iframes[x].getAttribute("id").toLowerCase().indexOf("adframe") >=0) {continue} else if(typeof irisqa_iframe != "undefined" && irisqa_iframe.body.innerHTML && irisqa_iframe.body.innerHTML.match(/AolHtml5Player/)) return x+1;}} catch(e){} } )();'
js_get_iframe_count = 'return document.getElementsByTagName("iframe").length;'
outdated_message = "Old version of adaptive is being used, they should update the script URL"



class Player(object):
    def __init__(self,driver,timeout,preroll_ads):
        self.driver = driver
        self.timeout = timeout
        self.preroll_ads = preroll_ads

    def is_element_present(self,locator):
        try:
            self.driver.find_element_by_css_selector(locator)
        except NoSuchElementException:
            return False
        return True

    def is_xelement_present(self,locator):
        try:
            self.driver.find_element_by_xpath(locator)
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
        global forward_xpath,js_forward, amp_forward_xpath
        el_list = self.driver.find_elements_by_xpath(amp_forward_xpath)
        plat_list = self.driver.find_elements_by_xpath(platform_forward)
        if len(el_list) > 0:
            forward_loc = amp_forward_xpath
        elif len(plat_list) > 0:
            forward_loc = platform_forward
        else:
            forward_loc = forward_xpath
        element = WebDriverWait(self.driver, 15).until(
			EC.presence_of_element_located((By.XPATH, forward_loc)))
        time.sleep(2)
        self.driver.execute_script(js_forward)

    def click_forward_playerx(self):
        global forward_xpath,js_forward, amp_forward_xpath
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
        global forward_xpath,amp_forward_xpath, forward_kmc,forward_amp,forward_display, forward
        print "waiting for skip forward to be present"
        if self.is_element_present(forward_kmc) and self.get_style_attr(forward_kmc) and "none" in self.get_style_attr(forward_kmc):
            forward_display = forward_kmc
            WebDriverWait(self.driver, self.timeout).until(
                    wait_for_forward_display()
                    )
        elif self.is_element_present(forward_amp) and self.get_style_attr(forward_amp) and "none" in self.get_style_attr(forward_amp):
            forward_display = forward_amp
            WebDriverWait(self.driver, self.timeout).until(
                wait_for_forward_display()
                )
        elif self.is_element_present(forward) and self.get_style_attr(forward) and "none" in self.get_style_attr(forward):
            forward_display = forward
            WebDriverWait(self.driver, self.timeout).until(
                wait_for_forward_display()
                )
        else:
            el_list = self.driver.find_elements_by_xpath(amp_forward_xpath)
            plat_list = self.driver.find_elements_by_xpath(platform_forward)
            if len(el_list) > 0:
                forward_loc = amp_forward_xpath
            elif len(plat_list) > 0:
                forward_loc = platform_forward
            else:
                forward_loc = forward_xpath
            element = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, forward_loc))
                )

    def wait_for_ad(self):
        global ad_bc, ad_banner, ad_caption
        if self.preroll_ads:
            print "checking if ad displayed"
            self.driver.implicitly_wait(1)
            if self.is_element_present(ad_banner):
                element = WebDriverWait(self.driver, self.timeout).until_not(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ad_banner))
                    )
            elif self.is_element_present(ad_caption):
                element = WebDriverWait(self.driver, self.timeout).until_not(
                    EC.visibility_of_element_located((PlayerLocators.VDB_AD_CAPTION))
                    )
            elif self.is_element_present(ad_bc):
                element = WebDriverWait(self.driver, self.timeout).until_not(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,ad_bc))
                    )
            elif self.is_xelement_present(ad_plat):
                element = WebDriverWait(self.driver, self.timeout).until_not(
                    EC.visibility_of_element_located((By.XPATH,ad_plat))
                    )
            self.driver.implicitly_wait(11)

    def click_back(self):
        global js_back, back_xpath, amp_back_xpath
        el_list = self.driver.find_elements_by_xpath(amp_back_xpath)
        plat_list = self.driver.find_elements_by_xpath(platform_back)
        if len(el_list) > 0:
            back_loc = amp_back_xpath
        elif len(plat_list) > 0:
            back_loc = platform_back
        else:
            back_loc = back_xpath
        element = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, back_loc)))
        self.driver.execute_script(js_back)

    def click_back_playerx(self):
        global js_back, back_xpath, amp_back_xpath
        el_list = self.driver.find_elements_by_xpath(amp_back_xpath)
        if len(el_list) > 0:
            back_loc = amp_back_xpath2
        else:
            back_loc = back_xpath2
        element = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, back_loc)))
        self.driver.execute_script(js_back2)

    def click_thumb_up(self):
		global js_thumb_up,thumb_up_xpath,amp_thumb_up_xpath
		el_list = self.driver.find_elements_by_xpath(amp_thumb_up_xpath)
		if len(el_list) > 0:
			thumb_up = amp_thumb_up_xpath
		else:
			thumb_up = thumb_up_xpath
		element = WebDriverWait(self.driver, 15).until(
				EC.presence_of_element_located((By.XPATH, thumb_up))
			)
		self.driver.execute_script(js_thumb_up)

    def click_thumb_up_playerx(self):
        global js_thumb_up,thumb_up_xpath,amp_thumb_up_xpath
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
		global js_thumb_down,thumb_down_xpath,amp_thumb_down_xpath
		el_list = self.driver.find_elements_by_xpath(amp_thumb_down_xpath)
		if len(el_list) > 0:
			thumb_down = amp_thumb_down_xpath
		else:
			thumb_down = thumb_down_xpath
		element = WebDriverWait(self.driver, 15).until(
				EC.presence_of_element_located((By.XPATH, thumb_down))
			)
		self.driver.execute_script(js_thumb_down)

    def click_thumb_down_playerx(self):
        global js_thumb_down,thumb_down_xpath,amp_thumb_down_xpath
        el_list = self.driver.find_elements_by_xpath(amp_thumb_down_xpath)
        if len(el_list) > 0:
            thumb_down = amp_thumb_down_xpath
        else:
            thumb_down = thumb_down_xpath
        element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, thumb_down))
            )
        self.driver.execute_script(js_thumb_down2)

    def click_end_next_slate(self,max_timeout):
		global end_next_slate
		element = WebDriverWait(self.driver, max_timeout).until(
				EC.element_to_be_clickable((By.CSS_SELECTOR, end_next_slate))
			)
		element.click()
		print "Clicked end next slate"

    def get_end_next_slate(self,max_timeout):
		global end_next_slate
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
        if "adaptive/iris.adaptive.js" in i:
            print outdated_message
        elif "player_plugins/iris.tv.jwplayer.min.js" in i:
            print outdated_message
        elif "kaltura/iris-kaltura.adaptive.min.js" in i:
            print outdated_message
        elif "brightcove/iris-bc.adaptive.min.js" in i:
            print outdated_message
	if '.css' not in combined_irisfiles:
		print "No Iris CSS was loaded (not added to HTML source code)\n"
	return combined_irisfiles

def check_platform_id(tempJson):
	r=0;
	for index,x in enumerate(tempJson):
		if not x.get("platform_id"):
			r+=1;
	return r

def check_experience(experience,tempJson):
    r=0;
    for index,x in enumerate(tempJson):
        if x.get("experience") and experience not in x.get("experience"):
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

def get_json_plat_ids(tempJson):
    platform_ids = []
    for p in tempJson:
        i = p.get("platform_id","")
        platform_ids.append(i)
    return platform_ids


def check_for_dup_recs(playlist, tempJson):
    dup = True
    og_plat_ids = get_json_plat_ids(playlist)
    for x in tempJson:
        plat_ids = get_platform_ids(tempJson)
        for y in plat_ids:
            if y not in og_plat_ids:
                dup = False
                break
        if dup == True:
            break   
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
        if x.get("start_up_next"):
            print "start_up_next: " + x.get("start_up_next","")
        if x.get("start_up_next_text"):
            print "Start up next text: " + x.get("start_up_next_text","")
        if x.get("start_up_next_text"):
            start_up_next_text = x.get("start_up_next_text","")
        if x.get("end_up_next_text"):
            end_up_next_text = x.get("end_up_next_text","")
        if x and x.get("end_up_next"):
            print "end_up_next: " + x.get("end_up_next","")
        if x.get("end_up_next_text"):
            print "End up next text: " + x.get("end_up_next_text","")
        if x.get("campaign_tracking"):
            print "Campaign tracking: " + x.get("campaign_tracking","")
        if x.get("experience"):
            print "experience: " + x.get("experience","")
        if x.get("disable_mobile_upnext"):
            print "disable_mobile_upnext: " + x.get("disable_mobile_upnext","")
        else:
            print "(upnext is disabled for mobile, parameter was not passed)"
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
