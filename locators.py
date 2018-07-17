from selenium.webdriver.common.by import By

play_list= ['div[role="button"][class*="jw-icon jw-icon-display"][aria-label="Start playback"]','div[role="button"][class*="jw-icon jw-icon-display"][aria-label="Start Playback"]',"*[class*='play-button']",'*[class*="icon-play"]','div[class*="play-icon"]',"*[id*='playButtonHolder']>canvas","*[id*='vjs-play-control vjs-control vjs-button']","button[aria-label='Start Playback']","button[class*='amp-pause-overlay']"]
ad_loc_list= ["div[class='akamai-ad']",'div[id*="adContainerkaltura_player"]','div[class*="ad-playing"]','div[class="amp-ads"]','div[class="ad-info-caption"]','div[class*="videoAdUi"]','div[class*="oo-player-skin-plugins oo-full oo-showing"]','div[class*="uvpjs--ad"]',"*[class*='jw-flag-ads']","div[class*='ad style-scope video-wrap on-top']",'div[id*="creative-iframe-container"]',"div[class*='plugin-googima']","div[class*='ima-ad-container']","div[class*='anv-ad-content']"]
ad_loc_xlist = ["//*[contains(text(),'Your video will resume in')]","//*[contains(text(),'Video will start in')]"]
video_playing_list=['div[class*="vjs-playing"]>video','div[class*="jw-state-playing"]>div>video','video[class*="uw-video"]',"video[class='video']","video[class='anv-video-content']","div[class*='uvpjs--streaming']"]
iframe_loc_list = ["iframe[class*='EmbedKalturaIframe']","iframe[src*='player.theplatform.com']","iframe[src*='players.brightcove.net']","div[class*='video-content']>div>iframe","iframe[id='anv_player']","div[class*='uw-iframe-video']>iframe"]
playing_loc_list =["div[class*='uvpjs--streaming']"]

class PlayerLocators(object):
    """A class for main page locators. All main page locators should come here"""
    NFL_ENABLE_IRIS = (By.ID, 'enable-iris-btn')
    NFL_MUTE = (By.CSS_SELECTOR, 'span[data-test-id="controls-volume"]')
    VDB_PLAYER_BAR = (By.CSS_SELECTOR, 'div[class="progress-bar-container"]')