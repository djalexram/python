from selenium.webdriver.common.by import By

class PlayerLocators(object):
    """A class for main page locators. All main page locators should come here"""
    NFL_ENABLE_IRIS = (By.ID, 'enable-iris-btn')
    NFL_MUTE = (By.CSS_SELECTOR, 'span[data-test-id="controls-volume"]')
    VDB_PLAYER_BAR = (By.CSS_SELECTOR, 'div[class="progress-bar-container"]')
    VDB_AD_CAPTION = (By.CSS_SELECTOR, 'div[class="ad-info-caption"]')
