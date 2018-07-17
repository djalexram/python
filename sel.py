import os
import pytest
import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from locators import PlayerLocators, ad_loc_list, ad_loc_xlist, play_list, video_playing_list, playing_loc_list
import time
import json
import sys


player = 2

#Other variables
arg_url = ""
iris_path = 'ovp.iris.tv'
iris_js = 'iris.adaptive.js'
iris_api = 'api.iris.tv'
iris_watch = 'iris.tv/watch'
iris_update = 'iris.tv/update'
iris_next = 'iris.tv/next'
bc_play="*[class*='play-button']"
chrome_termsID="terms_accept"
player_type='bc'
iframe=""
mute=""
ver=""
video1=False
campaign_tracking=False
watch_platform_id = ""
ssl=False
start_up_next_text=""
end_up_next_text=""
start_up_next=True
end_up_next=True
player_error = ["Setup Timeout Error: Setup took longer than 30 seconds to complete","something about your browser made us think you were a bot"]
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
platform_forward2 = "//canvas[@class='IconNext']"
platform_back2 = "//canvas[@class='IconPrevious']"
forward_amp = "div[id*='skip-forward']"
forward_display=""
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
platform_thumb_up = "//*[contains(@class,'ThumbsUp')]"
platform_thumb_down = "//*[contains(@class,'ThumbsDown')]"
start_next_slate='div[id$="start-next-slate"]'
end_next_slate='div[id$="end-next-slate"]'
start_next_slate_xpath="//div[contains(@id,'start-next-slate')]"
end_next_slate_xpath="//div[contains(@id,'end-next-slate')]"
pause = "button[class='vjs-play-control vjs-control vjs-button vjs-playing']"
bc_mute="//div[@class='vjs-control-bar']/div[1]"
o_mute = "//button[contains(@class,'vjs-mute-control')]"
vdb_mute='//div[contains(@class,"volume-button")]'
kmc_mute='//div[contains(@class,"comp volumeControl")]/button'
jw_mute='//div[contains(@class,"jw-icon jw-icon-tooltip jw-icon-volume")]'
tp_mute='//canvas[@class="IconUnmuted"]'
platform_mute = '//canvas[@class="IconUnmuted"]'
play = 'div[class*="vjs-big-play-button"]'
play2 = 'div[class*="icon-play"]'
svg_play = 'div[role="button"][aria-label="Start Playback"]'
jw_buffering = 'div[class*="jw-state-buffering"]'
js_forward = "if(document.querySelector('[id*=skip_forward]')) document.querySelector('[id*=skip_forward]').click(); else if(document.querySelector('[class*=skip-forward]')) document.querySelector('[class*=skip-forward]').click(); else if (document.querySelector('[class=IconNext]')) document.querySelector('[class=IconNext]').click(); else if (document.querySelector('[class=tpNext] > canvas')) document.querySelector('[class=tpNext] > canvas').click(); else if (document.querySelector('[id*=skip-forward]'))document.querySelector('[id*=skip-forward]').click(); else if (document.querySelector('[src*=\"brightcove/buttons/next.png\"]') != null) document.querySelector('[src*=\"brightcove/buttons/next.png\"]').click();"
js_forward2 = "if(document.querySelectorAll('[id*=skip_forward]')) document.querySelectorAll('[id*=skip_forward]')["+str(player-1)+"].click(); else if (document.querySelector('[class=IconNext]')) document.querySelector('[class=IconNext]')["+str(player-1)+"].click(); else if (document.querySelector('[class=tpNext] > canvas')) document.querySelector('[class=tpNext] > canvas')["+str(player-1)+"].click(); else if (document.querySelectorAll('[id*=skip-forward]')) document.querySelectorAll('[id*=skip-forward]')["+str(player-1)+"].click(); else if (document.querySelectorAll('[src*=\"brightcove/buttons/next.png\"]') != null) document.querySelectorAll('[src*=\"brightcove/buttons/next.png\"]')["+str(player-1)+"].click();"
js_back = "if(document.querySelector('[id*=skip_back]')) document.querySelector('[id*=skip_back]').click(); else if(document.querySelector('[class*=skip-back]')) document.querySelector('[class*=skip-back]').click(); else if (document.querySelector('[class=IconPrevious]')) document.querySelector('[class=IconPrevious]').click(); else if (document.querySelector('[class=tpPrevious] > canvas')) document.querySelector('[class=tpPrevious] > canvas').click(); else if(document.querySelector('[id*=skip-back]')) document.querySelector('[id*=skip-back]').click(); else if (document.querySelector('[src*=\"brightcove/buttons/prev.png\"]') != null) document.querySelector('[src*=\"brightcove/buttons/prev.png\"]').click();"
js_back2 = "if(document.querySelectorAll('[id*=skip_back]')) document.querySelectorAll('[id*=skip_back]')["+str(player-1)+"].click(); else if (document.querySelector('[class=IconPrevious]')) document.querySelector('[class=IconPrevious]').click(); else if (document.querySelector('[class=tpPrevious] > canvas')) document.querySelector('[class=tpPrevious] > canvas').click(); else if(document.querySelectorAll('[id*=skip-back]')) document.querySelectorAll('[id*=skip-back]')["+str(player-1)+"].click(); else if (document.querySelectorAll('[src*=\"brightcove/buttons/prev.png\"]') != null) document.querySelectorAll('[src*=\"brightcove/buttons/prev.png\"]')["+str(player-1)+"].click();"
js_thumb_down="if(document.querySelector('[id*=thumbs_down]') != null) document.querySelector('[id*=thumbs_down]').click(); else if(document.querySelector('[class*=thumbs-down]') != null) document.querySelector('[class*=thumbs-down]').click(); else if(document.querySelector('[class*=ThumbsDown]') != null) document.querySelector('[class*=ThumbsDown]').click(); else if(document.querySelector('[id*=thumbs-down]') != null) document.querySelector('[id*=thumbs-down]').click(); else if (document.querySelector('[src*=\"brightcove/buttons/dislike.png\"]') != null) document.querySelector('[src*=\"brightcove/buttons/dislike.png\"]').click();"
js_thumb_down2="if(document.querySelectorAll('[id*=thumbs_down]') != null) document.querySelectorAll('[id*=thumbs_down]')["+str(player-1)+"].click(); else if(document.querySelector('[class*=ThumbsDown]') != null) document.querySelector('[class*=ThumbsDown]').click(); else if(document.querySelectorAll('[id*=thumbs-down]') != null) document.querySelectorAll('[id*=thumbs-down]')[1].click(); else if (document.querySelectorAll('[src*=\"brightcove/buttons/dislike.png\"]') != null) document.querySelectorAll('[src*=\"brightcove/buttons/dislike.png\"]')["+str(player-1)+"].click();"
js_thumb_up="if(document.querySelector('[id*=thumbs_up]') != null) document.querySelector('[id*=thumbs_up]').click(); else if(document.querySelector('[class*=thumbs-up]') != null) document.querySelector('[class*=thumbs-up]').click(); else if(document.querySelector('[class*=ThumbsUp]') != null) document.querySelector('[class*=ThumbsUp]').click(); else if(document.querySelector('[id*=thumbs-up]') != null) document.querySelector('[id*=thumbs-up]').click(); else if (document.querySelector('[src*=\"brightcove/buttons/like.png\"]') != null) document.querySelector('[src*=\"brightcove/buttons/like.png\"]').click();"
js_thumb_up2="if(document.querySelectorAll('[id*=thumbs_up]') != null) document.querySelectorAll('[id*=thumbs_up]')["+str(player-1)+"].click(); else if(document.querySelector('[class*=ThumbsUp]') != null) document.querySelector('[class*=ThumbsUp]').click(); else if(document.querySelectorAll('[id*=thumbs-up]') != null) document.querySelectorAll('[id*=thumbs-up]')["+str(player-1)+"].click(); else if (document.querySelectorAll('[src*=\"brightcove/buttons/like.png\"]') != null) document.querySelectorAll('[src*=\"brightcove/buttons/like.png\"]')["+str(player-1)+"].click();"
js_player_type='return (function() { if (typeof bc != "undefined" || typeof bcPlayer != "undefined") return "bc"; else if(typeof tpScriptPath != "undefined" || typeof tpk != "undefined" || typeof tpController != "undefined") return "thePlatform"; else if(typeof anvp != "undefined" || typeof AnvatoPlayer != "undefined") return "anvato"; else if(typeof jwplayer != "undefined") return "jw"; else if(typeof kWidget != "undefined" || typeof KWidget != "undefined") return "kmc"; else if (typeof AKAMAI_MEDIA_PLAYER != "undefined" || typeof akamai != "undefined") return "amp"; else if (typeof Ooyala != "undefined" || typeof ooyala != "undefined") return "ooyala"; else if (typeof vdb != "undefined" || typeof vidible != "undefined") return "vdb"; else if (typeof tpScriptPath != "undefined" || typeof tpk != "undefined") return "tp"; else if (typeof THEOplayer != "undefined" || typeof theoplayer != "undefined") return "oplayer"; else if (typeof uvpjs != "undefined") return "uvpjs"; else return "unknown"} )();'
js_bc_v= 'return (function() { if (typeof bc != "undefined" && typeof bc.VERSION != "undefined") return bc.VERSION;} )(); '
js_play = "if(document.querySelector('[class*=play-button]') != null) document.querySelector('[class*=play-button]').click(); else if (document.querySelector('[class*=play-icon]') != null) document.querySelector('[class*=play-icon]').click(); else if (document.querySelector('[id*=playButtonHolder]>canvas') != null) document.querySelector('[id*=playButtonHolder]>canvas').click(); else if (document.querySelector('[class*=icon-play]') != null) document.querySelector('[class*=icon-play]').click(); else if(typeof document.getElementsByClassName('vjs-play-control vjs-control vjs-button')[0] != 'undefined') document.getElementsByClassName('vjs-play-control vjs-control vjs-button')[0].click();"
js_play2 = "if(document.querySelectorAll('[class*=play-button]') != null) document.querySelectorAll('[class*=play-button]')["+str(player-1)+"].click(); else if (document.querySelectorAll('[class*=play-icon]') != null) document.querySelectorAll('[class*=play-icon]')["+str(player-1)+"].click(); else if (document.querySelector('[id*=playButtonHolder]>canvas') != null) document.querySelector('[id*=playButtonHolder]>canvas').click(); else if (document.querySelectorAll('[class*=icon-play]') != null) document.querySelectorAll('[class*=icon-play]')["+str(player-1)+"].click(); else if(typeof document.querySelectorAll('[class=\"vjs-play-control vjs-control vjs-button\"]') != 'undefined') document.querySelectorAll('[class=\"vjs-play-control vjs-control vjs-button\"]')["+str(player-1)+"].click();"
js_playlist_len = 'return (function() { if(typeof iris != "undefined" && typeof iris.getPlaylist != "undefined") return iris.getPlaylist().length; else if (typeof IrisEngine != "undefined" && typeof IrisEngine.getPlaylist != "undefined") return IrisEngine.getPlaylist().length; else if (typeof iris1 != "undefined" && typeof iris1.getPlaylist != "undefined") return iris1.getPlaylist().length; else if (typeof iris_player != "undefined" && typeof iris_player.getPlaylist != "undefined") return iris_player.getPlaylist().length; else if (typeof iris_player != "undefined" && typeof iris_player.getPlaylist != "undefined") return iris_player.getPlaylist().length;} )();'
js_getIndex = 'return (function() { if(typeof iris != "undefined" && typeof iris.getCurrentIndex != "undefined") return iris.getCurrentIndex(); else if (typeof IrisEngine != "undefined" && typeof IrisEngine.getCurrentIndex != "undefined") return IrisEngine.getCurrentIndex(); else if (typeof iris1 != "undefined" && typeof iris1.getCurrentIndex != "undefined") return iris1.getCurrentIndex(); else if (typeof iris_player != "undefined" && typeof iris_player.getCurrentIndex != "undefined") return iris_player.getCurrentIndex(); else if (typeof iris_player != "undefined" && typeof iris_player.currentIndex != "undefined") return iris_player.currentIndex;} )();'
js_get_current_plat = 'return (function() { if(typeof iris != "undefined" && typeof iris.getPlaylist != "undefined") return iris.getPlaylist()[iris.getCurrentIndex()].platform_id; else if (typeof IrisEngine != "undefined" && typeof IrisEngine.getPlaylist != "undefined") return IrisEngine.getPlaylist()[IrisEngine.getCurrentIndex()].platform_id; else if (typeof iris1 != "undefined" && typeof iris1.getPlaylist != "undefined") return iris1.getPlaylist()[iris1.getCurrentIndex()].platform_id; else if (typeof iris_player != "undefined" && typeof iris_player.getPlaylist != "undefined") return iris_player.getPlaylist()[iris_player.getCurrentIndex()].platform_id; } )();'
js_get_asset_amp = 'return (function() { if(typeof akamai != "undefined" && typeof akamai.streamURL != "undefined") return akamai.streamURL;} )();'
js_get_video_src= 'return (function() { try{ if(typeof document.getElementsByTagName("video")[0] != "undefined" && document.getElementsByTagName("video")[0].getAttribute("src") != null) return document.getElementsByTagName("video")[0].getAttribute("src"); else if(typeof document.getElementsByTagName("video")[1] != "undefined" && document.getElementsByTagName("video")[1].getAttribute("src") != null) return document.getElementsByTagName("video")[1].getAttribute("src"); else if(document.getElementsByTagName("iframe")[0] != "undefined" && document.getElementsByTagName("iframe")[0].contentWindow.document.getElementsByTagName("video")[0] != "undefined") return document.getElementsByTagName("iframe")[0].contentWindow.document.getElementsByTagName("video")[0].getAttribute("src"); else if(document.getElementsByTagName("iframe")[1] != "undefined" && document.getElementsByTagName("iframe")[1].contentWindow.document.getElementsByTagName("video")[0] != "undefined") return document.getElementsByTagName("iframe")[1].contentWindow.document.getElementsByTagName("video")[0].getAttribute("src")} catch(e){} } )();'
js_get_iframe= 'return (function() {try{ var irisqa_iframes = document.getElementsByTagName("iframe"); for (var x=0; x<irisqa_iframes.length;x++) { if(irisqa_iframes[x].src && (irisqa_iframes[x].src == "" || irisqa_iframes[x].src == "javascript:false")) irisqa_iframe= irisqa_iframes[x].contentDocument || irisqa_iframes[x].contentWindow.document; if(irisqa_iframes[x].getAttribute("id")!= null && irisqa_iframes[x].getAttribute("id").toLowerCase().indexOf("adframe") >=0) {continue} else if(typeof irisqa_iframe != "undefined" && irisqa_iframe.body.innerHTML && irisqa_iframe.body.innerHTML.match(/AolHtml5Player/)) return x+1; else if(typeof irisqa_iframe != "undefined" && irisqa_iframe.body.innerHTML && irisqa_iframe.body.innerHTML.match(/anvato/)) return x+1;}} catch(e){} } )();'
js_get_iframe_count = 'return document.getElementsByTagName("iframe").length;'
js_get_iris_files = "return (function() { var files=[],stage='s3.amazonaws.com/iris-playground',prod='iris.tv'; var elscripts = [].slice.call(document.querySelectorAll(\"script[src*='\" + stage + \"'], script[src*='\" + prod + \"']\")); for (var i = 0, len = elscripts.length; i < len; i++) files.push(elscripts[i].src); var elcss = [].slice.call(document.querySelectorAll(\"link[href*='\" + stage + \"'], link[href*='\" + prod + \"']\")); for (var j = 0, len = elcss.length; j < len; j++) files.push(elcss[j].href); return files.join(','); } )();"
js_get_api_calls = "return (function() { var files=[],prod='api.iris.tv'; var elscripts = [].slice.call(document.querySelectorAll(\"script[src*='\" + prod + \"']\")); for (var i = 0, len = elscripts.length; i < len; i++) files.push(elscripts[i].src); return files.join(','); } )();"
js_get_ima3 = 'return (function() { if (typeof videojs != "undefined" && typeof videojs.players != "undefined" && typeof videojs.players[Object.keys(videojs.players)[0]].ima3 != "undefined") {return videojs.players[Object.keys(videojs.players)[0]].ima3.VERSION} } )();'
js_get_freewheel = 'return (function() { if (typeof videojs != "undefined" && typeof videojs.players != "undefined" && typeof videojs.players[Object.keys(videojs.players)[0]].FreeWheelPlugin != "undefined") {return videojs.players[Object.keys(videojs.players)[0]].FreeWheelPlugin.VERSION} } )();'
js_ad_platform = 'return (function() { if(typeof outbrain != "undefined") return "Outbrain"; else return false;} )();'
js_get_current_video = 'return (function() { if (typeof videojs != "undefined" && typeof videojs.players != "undefined") {return "PlatformID: " + videojs.players[Object.keys(videojs.players)[0]].mediainfo.id + ", " + videojs.players[Object.keys(videojs.players)[0]].mediainfo.name;} else if (typeof jwplayer != "undefined" && typeof jwplayer(0) != "undefined") {return "PlatformID: " + jwplayer(0).getPlaylistItem().mediaid + ", " + jwplayer(0).getPlaylistItem().title;} })();'
js_playing_state = 'return (function() { if (typeof jwplayer != "undefined" && jwplayer(0).getState() == "idle") {jwplayer(0).play();} else if (typeof jwplayer != "undefined" && (jwplayer(0).getState() == "playing" || jwplayer(0).getState() == "paused")) return true;  else if (typeof pp != "undefined" && typeof pp.getState != "undefined" && pp.getState() == "playing") return true; else if (document.querySelector("[class*=vjs-playing]")) return true; else if (document.querySelector("[class*=vjs-ad-playing]")) return true; else if (document.querySelector("[class*=akamai-playing]")) return true; else return false;} )(); '
js_ad_state = 'return (function() { if (document.querySelector("[class*=ad-playing]")) return true; else if (document.querySelector("[class*=jw-flag-ads]")) return true; else if (document.querySelector("[id*=adContainerkaltura_player]")) return true; else if (document.querySelector("[class*=\'oo-player-skin-plugins oo-full oo-showing\']")) return true; else if (document.querySelector("[class*=akamai-ad]")) return true; else if (document.querySelector("[class*=videoAdUi]")) return true; else if (document.querySelector("[class*=videoAdUi]")) return true; else if (document.querySelector("[class*=\'ad style-scope video-wrap on-top\']")) return true; else if (document.querySelector("[id*=creative-iframe-container]")) return true; else if (document.querySelector("[class*=anv-ad-content]")) return true;else if (document.querySelector("[class*=plugin-googima]")) return true;else if (document.querySelector("[class*=ima-ad-container]")) return true; else return false;} )(); '
js_mute = 'if (typeof jwplayer != "undefined") jwplayer(0).setMute(true); else if (typeof videojs != "undefined" && typeof videojs.players != "undefined" && typeof videojs.players[Object.keys(videojs.players)[0]] != "undefined") videojs.players[Object.keys(videojs.players)[0]].muted(true); else if (typeof pp != "undefined" && typeof pp.mute != "undefined") pp.mute(); else if (typeof amp != "undefined" && typeof amp.setMuted != "undefined") amp.setMuted(true); else if (typeof anvp != "undefined" && typeof anvp.getAll != "undefined") {var player1 = eval("anvp." + anvp.getAll()[0]); player1.mute()} '
js_jw_state = 'return (function() { if (typeof jwplayer != "undefined") return jwplayer(0).getState(); } )();'
js_jw_play = '(function() { if (typeof jwplayer != "undefined") jwplayer(0).play(); } )();'
js_get_ua = 'return window.navigator.userAgent;'
js_is_amp = 'return (function() { if (typeof amp != "undefined" || typeof AKAMAI_MEDIA_PLAYER != "undefined" || typeof akamai != "undefined") return true; else return false; } )();'
js_get_asset_id = '(function() { if (typeof jwplayer != "undefined") return jwplayer(0).getPlaylistItem().mediaid; else if(typeof videojs != "undefined" && videojs.players[Object.keys(videojs.players)[0]]) return videojs.players[Object.keys(videojs.players)[0]].mediainfo.id; else if (typeof pp != "undefined" && typeof pp.getEmbedCode != "undefined") return pp.getEmbedCode(); } )();'
js_scrub = '(function() { if (typeof jwplayer != "undefined" && jwplayer(0).getDuration() > 30) jwplayer(0).seek(jwplayer(0).getDuration()-20); else if (typeof amp != "undefined" && typeof amp.getDuration != "undefined" && amp.getDuration() > 30) amp.setCurrentTime(amp.getDuration()-20);else if(typeof videojs != "undefined" && videojs.players[Object.keys(videojs.players)[0]].mediainfo.duration > 30) videojs.players[Object.keys(videojs.players)[0]].currentTime(videojs.players[Object.keys(videojs.players)[0]].mediainfo.duration - 20);   })();'

outdated_message = "WARNING: Old version of adaptive is being used, they should update the script URL"

class Multiplayer():
    def __init__(self,player):
        self.player = player
        self.num = str(self.player-1)

    def set_m_xpath(self,xpath,player=None):
        if not player:
            player = self.player
        return "(" + xpath + ")["+str(player)+"]"

    def set_js_forward(self,num=None):
        if not num:
            num = self.num
        return "if(document.querySelectorAll('[id*=skip_forward]')) document.querySelectorAll('[id*=skip_forward]')["+num+"].click(); else if(document.querySelectorAll('[class*=skip-forward]')) document.querySelectorAll('[class*=skip-forward]')["+num+"].click(); else if (document.querySelector('[class=IconNext]')) document.querySelector('[class=IconNext]')["+num+"].click(); else if (document.querySelector('[class=tpNext] > canvas')) document.querySelector('[class=tpNext] > canvas')["+num+"].click(); else if (document.querySelectorAll('[id*=skip-forward]')) document.querySelectorAll('[id*=skip-forward]')["+num+"].click(); else if (document.querySelectorAll('[src*=\"brightcove/buttons/next.png\"]') != null) document.querySelectorAll('[src*=\"brightcove/buttons/next.png\"]')["+num+"].click();"

    def set_js_back(self,num=None):
        if not num:
            num = self.num
        return "if(document.querySelectorAll('[id*=skip_back]')) document.querySelectorAll('[id*=skip_back]')["+num+"].click(); else if(document.querySelectorAll('[class*=skip-back]')) document.querySelectorAll('[class*=skip-back]')["+num+"].click(); else if (document.querySelector('[class=IconPrevious]')) document.querySelector('[class=IconPrevious]')["+num+"].click(); else if (document.querySelector('[class=tpPrevious] > canvas')) document.querySelector('[class=tpPrevious] > canvas')["+num+"].click(); else if(document.querySelectorAll('[id*=skip-back]')) document.querySelectorAll('[id*=skip-back]')["+num+"].click(); else if (document.querySelectorAll('[src*=\"brightcove/buttons/prev.png\"]') != null) document.querySelectorAll('[src*=\"brightcove/buttons/prev.png\"]')["+num+"].click();"

    def set_js_thumb_down(self,num=None):
        if not num:
            num = self.num
        return "if(document.querySelectorAll('[id*=thumbs_down]') != null) document.querySelectorAll('[id*=thumbs_down]')["+num+"].click(); else if(document.querySelectorAll('[class*=thumbs-down]') != null) document.querySelectorAll('[class*=thumbs-down]')["+num+"].click(); else if(document.querySelector('[class*=ThumbsDown]') != null) document.querySelector('[class*=ThumbsDown]')["+num+"].click(); else if(document.querySelectorAll('[id*=thumbs-down]') != null) document.querySelectorAll('[id*=thumbs-down]')["+num+"].click(); else if (document.querySelectorAll('[src*=\"brightcove/buttons/dislike.png\"]') != null) document.querySelectorAll('[src*=\"brightcove/buttons/dislike.png\"]')["+num+"].click();"

    def set_js_thumb_up(self,num=None):
        if not num:
            num = self.num
        return "if(document.querySelectorAll('[id*=thumbs_up]') != null) document.querySelectorAll('[id*=thumbs_up]')["+num+"].click(); else if(document.querySelectorAll('[class*=thumbs-up]') != null) document.querySelectorAll('[class*=thumbs-up]')["+num+"].click(); else if(document.querySelector('[class*=ThumbsUp]') != null) document.querySelector('[class*=ThumbsUp]')["+num+"].click(); else if(document.querySelectorAll('[id*=thumbs-up]') != null) document.querySelectorAll('[id*=thumbs-up]')["+num+"].click(); else if (document.querySelectorAll('[src*=\"brightcove/buttons/like.png\"]') != null) document.querySelectorAll('[src*=\"brightcove/buttons/like.png\"]')["+num+"].click();"

    def set_video_src(self,num=None):
        if not num:
            num = self.num
        return 'return (function() { try{ if(typeof document.getElementsByTagName("video")['+num+'] != "undefined" && document.getElementsByTagName("video")['+num+'].getAttribute("src") != null) return document.getElementsByTagName("video")['+num+'].getAttribute("src"); else if(typeof document.getElementsByTagName("video")[1] != "undefined" && document.getElementsByTagName("video")[1].getAttribute("src") != null) return document.getElementsByTagName("video")[1].getAttribute("src"); else if(document.getElementsByTagName("iframe")[0] != "undefined" && document.getElementsByTagName("iframe")[0].contentWindow.document.getElementsByTagName("video")[0] != "undefined") return document.getElementsByTagName("iframe")[0].contentWindow.document.getElementsByTagName("video")[0].getAttribute("src"); else if(document.getElementsByTagName("iframe")[1] != "undefined" && document.getElementsByTagName("iframe")[1].contentWindow.document.getElementsByTagName("video")[0] != "undefined") return document.getElementsByTagName("iframe")[1].contentWindow.document.getElementsByTagName("video")[0].getAttribute("src")} catch(e){} } )();'


    def set_js_play(self,num=None):
        if not num:
            num = self.num
        return "if(document.querySelectorAll('[class*=play-button]') != null && typeof document.querySelectorAll('[class*=play-button]')["+num+"] != 'undefined') document.querySelectorAll('[class*=play-button]')["+num+"].click(); else if (document.querySelectorAll('div.play.clickable') != null && typeof document.querySelectorAll('div.play.clickable')[0] != 'undefined') document.querySelectorAll('div.play.clickable')[0].click(); else if (document.querySelectorAll('[class*=play-icon]') != null && typeof document.querySelectorAll('[class*=play-icon]')["+num+"] != 'undefined') document.querySelectorAll('[class*=play-icon]')["+num+"].click(); else if (document.querySelector('[id*=playButtonHolder]>canvas') != null && typeof document.querySelector('[id*=playButtonHolder]>canvas')["+num+"] != 'undefined') document.querySelector('[id*=playButtonHolder]>canvas')["+num+"].click(); else if (document.querySelectorAll('[class*=icon-play]') != null && typeof document.querySelectorAll('[class*=icon-play]')["+num+"] != 'undefined') document.querySelectorAll('[class*=icon-play]')["+num+"].click(); else if(typeof document.querySelectorAll('[class=\"vjs-play-control vjs-control vjs-button\"]')["+num+"] != 'undefined') document.querySelectorAll('[class=\"vjs-play-control vjs-control vjs-button\"]')["+num+"].click();"


class Player(object):
    def __init__(self,driver,timeout,preroll_ads,player):
        self.driver = driver
        self.timeout = timeout
        self.preroll_ads = preroll_ads
        self.multiplayer = Multiplayer(player)
        self.player = player

    def is_element_present(self,locator):
        try:
            self.driver.find_element_by_css_selector(locator)
        except NoSuchElementException:
            return False
        return True

    def get_element_attribute(self,locator,attr):
        try:
            temp = self.driver.find_element_by_css_selector(locator)
            if temp and temp.get_attribute(attr):
            	return temp.get_attribute(attr)
        except NoSuchElementException:
            return False

    def is_xelement_present(self,locator):
        try:
            self.driver.find_element_by_xpath(locator)
        except NoSuchElementException:
            return False
        return True

    def get_style_attr(self,element):
        try:
            t = False
            #e = self.driver.find_element_by_css_selector(locator)
            s = element.get_attribute("style")
            b = element.value_of_css_property("display")
            if s and 'display' in s:
                t=s.split(':')[1]
            elif b:
                t=b
        except NoSuchElementException:
            return False
        return t

    def click_forward(self):
        global forward_xpath,js_forward, amp_forward_xpath
        self.driver.implicitly_wait(1)
        el_list = self.driver.find_elements_by_xpath(amp_forward_xpath)
        plat_list = self.driver.find_elements_by_xpath(platform_forward)
        plat_list2 = self.driver.find_elements_by_xpath(platform_forward2)
        if len(el_list) ==1:
            forward_loc = self.multiplayer.set_m_xpath(amp_forward_xpath,1)
        elif len(plat_list) ==1:
            forward_loc = self.multiplayer.set_m_xpath(platform_forward,1)
        elif len(el_list)>0 and el_list[self.player-1]:
            forward_loc = self.multiplayer.set_m_xpath(amp_forward_xpath)
        elif len(plat_list)>0 and plat_list[self.player-1]:
            forward_loc = self.multiplayer.set_m_xpath(platform_forward)
        elif len(plat_list2)>0 and plat_list2[self.player-1]:
            forward_loc = self.multiplayer.set_m_xpath(platform_forward2)
        else:
            forward_loc = self.multiplayer.set_m_xpath(forward_xpath)
        element = WebDriverWait(self.driver, 15).until(
			EC.presence_of_element_located((By.XPATH, forward_loc)))
        print "clicking forward"
        self.driver.execute_script(self.multiplayer.set_js_forward())
        self.driver.implicitly_wait(11)
        time.sleep(1)

    def click_forward_playerx(self):
        global forward_xpath,js_forward, amp_forward_xpath
        el_list = self.driver.find_elements_by_xpath(amp_forward_xpath)
        if len(el_list) > 0:
            forward_loc = amp_forward_xpath2
        else:
            forward_loc = forward_xpath2
        element = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, forward_loc)))
        self.driver.execute_script(js_forward2)
        time.sleep(1)

    def wait_for_forward(self):
        global forward_xpath,amp_forward_xpath, forward_kmc,forward_amp,forward_display, forward
        print "waiting for skip forward to be present"
        self.driver.implicitly_wait(1)
        player_num = self.player-1
        kmc_list = self.driver.find_elements_by_css_selector(forward_kmc)
        amp_list = self.driver.find_elements_by_css_selector(forward_amp)
        forward_list = self.driver.find_elements_by_css_selector(forward)
        if len(kmc_list) >0 and self.get_style_attr(kmc_list[0]) and "none" in self.get_style_attr(kmc_list[0]):
            WebDriverWait(self.driver, self.timeout).until(
                wait_for_forward_display(kmc_list[0])
                )
        elif len(amp_list) >0 and amp_list[player_num] and self.get_style_attr(amp_list[player_num]) and "none" in self.get_style_attr(amp_list[player_num]):
            WebDriverWait(self.driver, self.timeout).until(
                wait_for_forward_display(amp_list[player_num])
                )
        elif len(forward_list) >0 and forward_list[player_num] and self.get_style_attr(forward_list[player_num]) and "none" in self.get_style_attr(forward_list[player_num]):
            WebDriverWait(self.driver, self.timeout).until(
                wait_for_forward_display(forward_list[player_num])
                )
        else:
            el_list = self.driver.find_elements_by_xpath(amp_forward_xpath)
            plat_list = self.driver.find_elements_by_xpath(platform_forward)
            plat_list2 = self.driver.find_elements_by_xpath(platform_forward2)
            if len(el_list) == 1:
                forward_loc = self.multiplayer.set_m_xpath(amp_forward_xpath,1)
            elif len(plat_list) == 1:
                forward_loc = self.multiplayer.set_m_xpath(platform_forward,1)
            elif len(plat_list2) == 1:
                forward_loc = self.multiplayer.set_m_xpath(platform_forward2,1)
            elif len(el_list)>0 and el_list[player_num]:
                forward_loc = self.multiplayer.set_m_xpath(amp_forward_xpath)
            elif len(plat_list)>0 and plat_list[player_num]:
                forward_loc = self.multiplayer.set_m_xpath(platform_forward)
            elif len(plat_list2)>0 and plat_list2[player_num]:
                forward_loc = self.multiplayer.set_m_xpath(platform_forward2)
            else:
                forward_loc = self.multiplayer.set_m_xpath(forward_xpath)
            element = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, forward_loc))
                )
        self.driver.implicitly_wait(11)

    def wait_for_ad(self):
        global ad_bc, ad_banner, ad_caption
        if self.preroll_ads:
        	state = self.driver.execute_script(js_ad_state)
        	ad_timeout = self.timeout + 40
        	print "checking if ad displayed"
        	self.driver.implicitly_wait(0.6)
        	status=0
        	if state:
        		for loca in ad_loc_list:
        			if self.is_element_present(loca):
        				element = WebDriverWait(self.driver, ad_timeout).until_not(
        					EC.visibility_of_element_located((By.CSS_SELECTOR, loca))
        				)
        				#print loca
        				status=1
        				break
        	if status ==0:
        		for xloca in ad_loc_xlist:
        			if self.is_xelement_present(xloca):
        				element = WebDriverWait(self.driver, ad_timeout).until_not(
        					EC.visibility_of_element_located((By.XPATH,xloca))
        				)
        				#print xloca
        				break
        	self.driver.implicitly_wait(11)

    def wait_for_playing(self,locator):
        if self.preroll_ads:
        	print "waiting for element w/ playing class"
        	ad_timeout = self.timeout + 40
        	self.driver.implicitly_wait(0.5)
        	if self.is_element_present(locator):
        		element = WebDriverWait(self.driver, ad_timeout).until(
        			EC.presence_of_element_located((By.CSS_SELECTOR, locator))
        			)
        	self.driver.implicitly_wait(11)

    def click_play(self):
        self.driver.implicitly_wait(0.5)
        print "looking for play button"
        for p in play_list:
            if self.is_element_present(p):
                self.driver.find_element_by_css_selector(p).click()
                break
        self.driver.implicitly_wait(11)

    def check_if_paused(self):
        state = self.driver.execute_script(js_jw_state)
        if state and state == "paused":
        	print "Player was paused"
        	self.driver.execute_script(js_jw_play)
        time.sleep(.5)
        state = self.driver.execute_script(js_jw_state)
        if state and state == "paused":
        	print "Player paused a second time"
        	self.driver.execute_script(js_jw_play)
        	#self.driver.refresh()

    def scrub(self):
        self.driver.execute_script(js_scrub)

    def click_back(self):
        global js_back, back_xpath, amp_back_xpath
        self.driver.implicitly_wait(1)
        el_list = self.driver.find_elements_by_xpath(amp_back_xpath)
        plat_list = self.driver.find_elements_by_xpath(platform_back)
        plat_list2 = self.driver.find_elements_by_xpath(platform_back2)
        if len(el_list) ==1:
            back_loc =self.multiplayer.set_m_xpath(amp_back_xpath,1)
        elif len(plat_list) ==1:
            back_loc = self.multiplayer.set_m_xpath(platform_back,1)
        elif len(plat_list2) ==1:
            back_loc = self.multiplayer.set_m_xpath(platform_back2,1)
        elif len(el_list)>0 and el_list[self.player-1]:
            back_loc = self.multiplayer.set_m_xpath(amp_back_xpath)
        elif len(plat_list)>0 and plat_list[self.player-1]:
            back_loc = self.multiplayer.set_m_xpath(platform_back)
        elif len(plat_list2)>0 and plat_list2[self.player-1]:
            back_loc = self.multiplayer.set_m_xpath(platform_back2)
        else:
            back_loc = self.multiplayer.set_m_xpath(back_xpath)
        element = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, back_loc)))
        print "clicking back"
        self.driver.execute_script(self.multiplayer.set_js_back())
        self.driver.implicitly_wait(11)
        time.sleep(.5)

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
        time.sleep(.5)

    def click_thumb_up(self):
        global js_thumb_up,thumb_up_xpath,amp_thumb_up_xpath
        self.driver.implicitly_wait(1)
        el_list = self.driver.find_elements_by_xpath(amp_thumb_up_xpath)
        plat_list = self.driver.find_elements_by_xpath(platform_thumb_up)
        if len(el_list)==1:
            thumb_up = self.multiplayer.set_m_xpath(amp_thumb_up_xpath,1)
        elif len(plat_list) ==1:
            thumb_up = self.multiplayer.set_m_xpath(platform_thumb_up,1)
        elif len(el_list)>0 and el_list[self.player-1]:
            thumb_up = self.multiplayer.set_m_xpath(amp_thumb_up_xpath)
        elif len(plat_list)>0 and plat_list[self.player-1]:
            thumb_up = self.multiplayer.set_m_xpath(platform_thumb_up)
        else:
            thumb_up = self.multiplayer.set_m_xpath(thumb_up_xpath)
        element = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, thumb_up))
            )
        print "clicking thumbs up"
        self.driver.execute_script(self.multiplayer.set_js_thumb_up())
        self.driver.implicitly_wait(11)

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
        self.driver.implicitly_wait(1)
        el_list = self.driver.find_elements_by_xpath(amp_thumb_down_xpath)
        plat_list = self.driver.find_elements_by_xpath(platform_thumb_down)
        if len(el_list)==1:
            thumb_down = self.multiplayer.set_m_xpath(amp_thumb_down_xpath,1)
        elif len(plat_list) == 1:
            thumb_down = self.multiplayer.set_m_xpath(platform_thumb_down,1)
        elif len(el_list)>0 and el_list[self.player-1]:
            thumb_down = self.multiplayer.set_m_xpath(amp_thumb_down_xpath)
        elif len(plat_list)>0 and plat_list[self.player-1]:
            thumb_down = self.multiplayer.set_m_xpath(platform_thumb_down)
        else:
            thumb_down = self.multiplayer.set_m_xpath(thumb_down_xpath)
        element = WebDriverWait(self.driver, 15).until(
				EC.presence_of_element_located((By.XPATH, thumb_down))
			)

        print "clicking thumbs down"
        self.driver.execute_script(self.multiplayer.set_js_thumb_down())
        self.driver.implicitly_wait(11)
        time.sleep(.5)

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
        time.sleep(.5)

    def click_end_next_slate(self,max_timeout):
		global end_next_slate
		element = WebDriverWait(self.driver, max_timeout).until(
				EC.element_to_be_clickable((By.XPATH, end_next_slate_xpath))
			)
		element.click()
		print "Clicked end next slate"

    def get_end_next_slate(self,max_timeout):
		global end_next_slate
		element = WebDriverWait(self.driver, max_timeout).until(
				EC.element_to_be_clickable((By.XPATH, end_next_slate_xpath))
			)
		temp = element.text 
		element.click()
		print "Clicked end next slate"
		return temp

    def click_start_next_slate(self):
		global start_next_slate
		element = WebDriverWait(self.driver, 30).until(
				EC.element_to_be_clickable((By.XPATH, start_next_slate_xpath))
			)
		element.click()
		print "Clicked start next slate"

    def get_start_next_slate(self):
		global start_next_slate
		element = WebDriverWait(self.driver, 30).until(
				EC.element_to_be_clickable((By.XPATH, start_next_slate_xpath))
			)
		temp = element.text
		element.click()
		print "Clicked start next slate"
		return temp

    def get_playlist_platformID(self,num):
    	playlist_length = self.driver.execute_script(js_playlist_len)
    	if playlist_length and int(playlist_length) > 1:
    		code = 'return (function() { if(typeof iris != "undefined" && typeof iris.getPlaylist != "undefined") return iris.getPlaylist()['+ str(num) +'].platform_id; else if (typeof IrisEngine != "undefined" && typeof IrisEngine.getPlaylist != "undefined") return IrisEngine.getPlaylist()['+ str(num) +'].platform_id; else if (typeof iris1 != "undefined" && typeof iris1.getPlaylist != "undefined") return iris1.getPlaylist()['+ str(num) +'].platform_id; else if (typeof iris_player != "undefined" && typeof iris_player.getPlaylist != "undefined") return iris_player.getPlaylist()['+ str(num) +'].platform_id; } )();'
    		platID = self.driver.execute_script(code)
    		if platID:
    			return platID
        else:
        	print "Looks like there was no Iris global variable"
        	return False

    def get_playlist_len(self):
        playlist_length = self.driver.execute_script(js_playlist_len)
        if playlist_length and int(playlist_length) > 1:
            return int(playlist_length)
        else:
            return False

    def get_current_platformID(self):
        platID = self.driver.execute_script(js_get_current_plat)
        if platID:
            return platID
        else:
        	tempID = self.driver.execute_script(js_get_asset_id)
        	if tempID:
        		return tempID
        	else:
        		return False

    def get_currentIndex(self):
        i = self.driver.execute_script(js_getIndex)
        if i:
            return i
        else:
            return False

    def get_first_video(self):
        global video1
        self.driver.implicitly_wait(0.5)
        video1 = self.driver.execute_script(self.multiplayer.set_video_src())
        for loca in video_playing_list:
        	if self.is_element_present(loca) and self.get_element_attribute(loca,"src"):
        		video1 = self.get_element_attribute(loca,"src")
        		#print loca
        		break
        self.driver.implicitly_wait(11)
        if video1:
            print "Video: " + video1
            return video1
        else:
            return False

    def get_iris_files(self):
        global js_get_iris_files
        return self.driver.execute_script(js_get_iris_files)

    def get_iris_cookie(self,cookies):
    	value = False
    	try:
    		for cookie in cookies:
    			if bool(cookie.get("name")) and cookie['name'] == 'iris_user_id':
    				print "\nCookie iris_user_id: " + cookie['value']
    				value = cookie['value']
    				break
    	except:
    		print "get_iris_cookie exception"
    	return value


    def get_js_api_calls(self):
    	src =[]
    	api_calls = self.driver.execute_script(js_get_api_calls).split(",")
    	if api_calls:
    		for a in api_calls:
    			src.append(a)
    			if "/watch" in a or "/next" in a:
    				print "\n" + a
    	return src

    def get_query_strings(self,urls):
    	for u in urls:
    		parsed = urlparse.urlparse(u)
    		params = urlparse.parse_qsl(parsed.query)
    		if "/watch" in u:
    			print "\nWATCH CALL:"
    		elif "/next" in u:
    			print "\nNEXT CALL:"
    		elif "/update" in u:
    			print "\nUPDATE CALL:"
    		for x,y in params:
    			print x +" = "+y


    def check_for_error(self,path):
        error=False
        html = self.driver.page_source
        for e in player_error:
            if e in html:
                driver.save_screenshot(get_screenshot_filename(path))
                error = e
                break
        return error
        

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
    def __init__(self, player):
        self.player = player

    def __call__(self, driver):
    	self.driver = driver
        global video1
        multiplayer = Multiplayer(self.player)
        try:
        	video = driver.execute_script(multiplayer.set_video_src())
        	driver.implicitly_wait(0.5)
        	for loca in video_playing_list:
        		element = self.is_element_present(loca)
        		if element and element.get_attribute("src"):
        			video = element.get_attribute("src")
        			break
        	self.driver.implicitly_wait(11)
        	return video1 != video
        except TimeoutException:
            print "Verify max_timeout is setup correctly for length of first video"
            return 0

    def is_element_present(self,locator):
        try:
            elm = self.driver.find_element_by_css_selector(locator)
        except NoSuchElementException:
            return False
        return elm

class wait_for_page_load():
    def __call__(self, driver):
        try:
            page_state = driver.execute_script('return document.readyState;')
            return page_state == 'complete'
        except TimeoutException:
            print "Verify max_timeout is setup correctly"
            return False

class wait_for_forward_display():
    def __init__(self, element):
        self.el = element

    def __call__(self, driver):
        try:
            t= "none"
            #e = driver.find_element_by_css_selector(self.locator)
            s = self.el.get_attribute("style")
            if 'display' in s:
                t=s.split(':')[1]
            return "block" in t
        except TimeoutException:
            print "Verify max_timeout is setup correctly"
            return False

class wait_for_first_video():
    def __init__(self, player):
        self.player = player

    def __call__(self, driver):
    	self.driver = driver
        try:
            multiplayer = Multiplayer(self.player)
            temp = driver.execute_script(multiplayer.set_video_src())
            driver.implicitly_wait(0.5)
            for loca in video_playing_list:
            	element = self.is_element_present(loca)
            	if element and element.get_attribute("src"):
        			temp = element.get_attribute("src")
        			break
        	driver.implicitly_wait(11)
            if temp and temp != "":
                video = True
                print "Video: " + temp
            else:
                video = False
            return video == True
        except TimeoutException:
            print "Verify max_timeout is setup correctly for length of first video"
            return False

    def is_element_present(self,locator):
        try:
            elm = self.driver.find_element_by_css_selector(locator)
        except NoSuchElementException:
            return False
        return elm

def get_screenshot_filename(path):
    filename = path+ "/reports/screenshot" + "-" + str(int(time.time())) + ".png"
    print "\nScreenshot: " + filename
    return filename

def print_responses(responses):
    for x in responses:
        if x.get("url"):
            print "\n" + x.get("url").encode('ascii', 'ignore')
        if x.get("response"):
            print "RESPONSE:\n" + x.get("response").encode('ascii', 'ignore')

def get_api_calls(tempJson,user_id=None):
	status = True
	for x in tempJson:
		if "/watch" in x.get("url",""):
			print "\nWATCH CALL: " 
			print "startedDateTime: " + x.get("startedDateTime","")
			print "Platform id: " + x.get("platform_id","")
			print "Client token: " + x.get("client_token","")
			if x.get("start_up_next"):
				print "start_up_next: " + x.get("start_up_next","")
			if x.get("set_cookie"):
				print "set_cookie: " + x.get("set_cookie","")
			if x.get("ssl"):
				print "ssl: " + x.get("ssl","")
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
			if x.get("perform_player"):
				print "perform_player: " + x.get("perform_player","")
			if x.get("onceux"):
				print "onceux: " + x.get("onceux","")
			if x.get("debug"):
				print "debug: " + x.get("debug","")
			if x.get("global"):
				print "global: " + x.get("global","")
			if x.get("disable_mobile_upnext"):
				print "disable_mobile_upnext: " + x.get("disable_mobile_upnext","")
			else:
				print "(upnext is disabled for mobile, parameter was not passed)"
		elif "/next" in x.get("url",""):
			if user_id and user_id != x.get("user_id",""):
				status = False
			print "\nNEXT CALL: "
			print "startedDateTime: " + x.get("startedDateTime","")
			print "Platform id: " + x.get("platform_id","")
			print "Client token: " + x.get("client_token","")
			if x.get("start_up_next_text"):
				print "Start up next text: " + x.get("start_up_next_text","")
			if x.get("end_up_next_text"):
				print "End up next text: " + x.get("end_up_next_text","")
			print "Campaign tracking: " + x.get("campaign_tracking","")
			if x.get("experience"):
				print "experience: " + x.get("experience","")
		elif "/update" in x.get("url",""):
			if user_id and user_id != x.get("user_id",""):
				status = False
        	print "\nUPDATE CALL: " 
        	print "startedDateTime: " + x.get("startedDateTime","")
        	print "Platform id: " + x.get("platform_id","")
        	if x.get("title"):
        		print "Asset title: " + x.get("title","")
        	if x.get("behavior[percentage_watched]"):
        		print "behavior[percentage_watched]: " + x.get("behavior[percentage_watched]","")
        	if x.get("behavior[seconds_watched]"):
        		print "behavior[seconds_watched]: " + x.get("behavior[seconds_watched]","")
        	if x.get("metrics_only"):
        		print "metrics_only: " + x.get("metrics_only","")
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
        return status

def check_iris_files(iris_files,ssl=None):
    if len(iris_files) > 0:
        combined_irisfiles = '\t'.join(iris_files)
    else:
        print "No Iris files found/loaded"
        combined_irisfiles = ""
    for i in iris_files:
        if "adaptive/iris.adaptive.js" in i:
            print outdated_message
        elif "standard/iris-nojquery.min.js" in i:
            print outdated_message
        elif "player_plugins/iris.tv.jwplayer.min.js" in i:
            print outdated_message
        elif "cloudfront.net/cosmos/iris.adaptive.js" in i:
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
		if x.get("behavior[percentage_watched]") and "1.0" not in x.get("behavior[percentage_watched]") and x.get("behavior[percentage_watched]") != "NaN":
			p = x.get("behavior[percentage_watched]").encode('ascii', 'ignore')

			if "0" in p and int(p.replace("0.","")) in range (23,29):
				watched.append(p)
			elif "0" in p and int(p.replace("0.","")) in range (48,60):
				watched.append(p)
			elif "0" in p and int(p.replace("0.","")) in range (70,80):
				watched.append(p)
			elif "0" not in p:
				pytest.fail("ERROR: Looks like we reached an edge case, percentage watched: " + p)
	return watched

def get_seconds_watched(tempJson):
    watched = []
    for x in tempJson:
        m = x.get("metrics_only","false").encode('ascii', 'ignore')
        if x.get("behavior[seconds_watched]") and x.get("behavior[seconds_watched]") != "0" and m == "true":
            p = x.get("behavior[percentage_watched]").encode('ascii', 'ignore')
            if p == "1.00":
                continue
            s = x.get("behavior[seconds_watched]").encode('ascii', 'ignore')
            if s and s != "0":
                t = s[:s.find(".")]
            m = x.get("metrics_only","false").encode('ascii', 'ignore')
            if int(p.replace("0.","")) in range (23,28):
                continue
            elif int(p.replace("0.","")) in range (48,60):
                continue
            elif int(p.replace("0.","")) in range (70,82):
                continue
            elif 3 <= int(t) <=4:
                watched.append(s)
            elif 4 <= int(t) <= 6:
                watched.append(s)
            elif 9 <= int(t) <=11:
                watched.append(s)
            elif 14 <= int(t) <=16:
                watched.append(s)
            elif 29 <= int(t) <=31:
                watched.append(s)
        else:
            continue
    return watched

def get_sec_beacon(x):
    m = x.get("metrics_only","false").encode('ascii', 'ignore')
    if x.get("behavior[seconds_watched]") and x.get("behavior[seconds_watched]") != "0" and m == "true":
        p = x.get("behavior[percentage_watched]").encode('ascii', 'ignore')
        if p == "1.00":
            return p
        s = x.get("behavior[seconds_watched]").encode('ascii', 'ignore')
        if s and s != "0":
            t = s[:s.find(".")]
        if int(p.replace("0.","")) in range (23,28):
            return 0
        elif int(p.replace("0.","")) in range (48,60):
            return 0
        elif int(p.replace("0.","")) in range (70,82):
            return 0
        elif 3 <= int(t) <=4:
            return int(t)
        elif 4 <= int(t) <= 6:
            return int(t)
        elif 9 <= int(t) <=11:
            return int(t)
        elif 14 <= int(t) <=16:
            return int(t)
        elif 29 <= int(t) <=31:
            return int(t)

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

def get_asset_urls(tempJson):
    djson = get_json(tempJson)
    playlist = djson["next"]
    urls = []
    cms= False
    for p in playlist:
    	if p.get("platform") and p.get("platform") == "brightcovecms":
    		cms = True
    		continue
        if p.get("content_url") and p.get("content_url") is not None:
            u = p.get("content_url","").encode('ascii', 'ignore')
            if "http:" in u or "https:" in u:
                urls.append(u)
    if cms:
    	print "\nPlatform is brightcovecms"
    return urls

def get_asset_images(tempJson):
    djson = get_json(tempJson)
    playlist = djson["next"]
    urls = []
    for p in playlist:
        if p.get("image_url") and  p.get("image_url") is not None:
            u = p.get("image_url","").encode('ascii', 'ignore')
            if "http:" in u or "https:" in u:
            	urls.append(u)
    if not urls:
    	print "\nWARNING: looks like no thumbnail images found"
    return urls

def get_vast_tag(tempJson):
    playlist = tempJson["next"]
    for p in playlist:
        if p.get("rule_settings"):
            temp = p.get("rule_settings")
            if temp.get("vast"):
                print "\nVAST TAG FOUND IN WATCH CALL:\n" + str(json.dumps(p, ensure_ascii=True))
                return temp.get("vast")
        else:
            return False

def get_json_plat_ids(tempJson):
    platform_ids = []
    for p in tempJson:
        i = p.get("platform_id","")
        if i in platform_ids:
            print "\nWARNING: duplicate asset found in watch call, platform_id: " + i
            print str(json.dumps(tempJson, ensure_ascii=True)) + "\n"
        platform_ids.append(i)
    return platform_ids

def check_for_dup_asset(tempJson):
    stat = False
    platform_ids = []
    for p in tempJson:
        i = p.get("platform_id","").encode('ascii', 'ignore')
        if i in platform_ids:
            stat = True
            break
        platform_ids.append(i)
    return stat

def check_for_dup_recs(playlist, tempJson):
    dup = False
    recs = []
    og_plat_ids = get_json_plat_ids(playlist)
    for x in tempJson:
        plat_ids = get_platform_ids(tempJson)
        for y in plat_ids:
            if y in og_plat_ids:
                dup = True
                if y not in recs:
                	recs.append(y.encode('ascii', 'ignore'))
                continue
        if dup:
        	dup = recs
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

def get_cms_ids(urls):
    platform_ids = []
    for url in urls:
        if "brightcove.com" in url:
            temp = url[url.index("/videos/")+8:]
            platform_ids.append(temp)
        elif "jwplatform.com" in url:
            temp = url[url.index("/feeds/")+7:url.index(".json")]
            platform_ids.append(temp)
    return platform_ids
	
def set_watch_call_params(tempJson):
    global campaign_tracking, end_up_next_text, start_up_next_text, watch_platform_id
    if not tempJson:
        print "Watch call not found"
        return False
    config = dict()
    for index,x in enumerate(tempJson):
    	if x.get("user_id"):
            config['user_id'] = x.get("user_id","")
        if x.get("start_up_next_text"):
            start_up_next_text = x.get("start_up_next_text","")
            config['start_up_next_text'] = x.get("start_up_next_text","")
        if x.get("platform_id"):
            watch_platform_id = x.get("platform_id","")
            config['watch_platform_id'] = x.get("platform_id","")
        if x.get("end_up_next_text"):
            end_up_next_text = x.get("end_up_next_text","")
            config['end_up_next_text'] = x.get("end_up_next_text","")
        if x.get("campaign_tracking","") == "true":
            campaign_tracking = True
            config['campaign_tracking'] = True
        else:
            campaign_tracking = False
            config['campaign_tracking'] = False
        if x.get("start_up_next","") == "true":
            start_up_next = True
            config['start_up_next'] = True
        else:
            start_up_next = False
            config['start_up_next'] = False
        if x.get("end_up_next","") == "true":
            end_up_next = True
            config['end_up_next'] = True
        else:
            end_up_next = False
            config['end_up_next'] = False
        if x.get("ssl","") == "true":
            ssl = True
            config['ssl'] = True
        else:
            ssl = False
            config['ssl'] = False
        if x.get("set_cookie","") == "false":
            config['set_cookie'] = False
        else:
            config['set_cookie'] = True
    return config

def total_calls(watch_calls,update_calls,next_calls):
	print "\nTotal watch calls " + str(len(watch_calls))
	print "Total update calls " + str(len(update_calls))
	print "Total next calls " + str(len(next_calls))

def get_plugin_ver(logfile):
    logfile= os.getcwd() + "/browser_logs/"+logfile
    log={}
    ima3=[]
    error=[]
    ima3_complete=0
    with open (logfile, "r") as myfile:
        logs=myfile.readlines()
        for x in logs:
            if "Plugin Version:" in x or "Library Version:" in x:
                print "\n" + x
            elif "jwplayer is not defined" in x and x not in error:
                print "\n" + x
                error.append(x)
            elif "ima3-ad-error" in x:
            	ima3.append(x)
            elif "ima3-complete" in x:
            	ima3_complete += 1
            elif "onVideoEnd" in x and x not in error:
            	print "\n" + x
                error.append(x)
            elif "trackComplete" in x and x not in error:
            	print "\n" + x
                error.append(x)

    if ima3:
    	log["ima3-error"] = ima3
    	print str(ima3) + "\n"
    if error:
    	log["error"] = error
    	for e in error:
    		if "jwplayer is not defined" in e:
    			print "WARNING: JW player is not loading, problem w/ JW Javascript code"
    			break

    if ima3_complete >0:
    	log["ima3_complete"] = ima3_complete
    	print "Completed pre-roll ads: " + str(ima3_complete)
    return log

