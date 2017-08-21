
MAC OS SETUP

Install Apple Xcode and accept license
sudo xcodebuild -license accept

Install Homebrew
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Install updated Python which includes pip.
brew install python

PIP INSTALL
Installing with pip (you may have to install using sudo for some items)
pip install selenium
pip install browsermob-proxy
pip install pytest
pip install pytest-html
pip install pyvirtualdisplay

Geckdriver is required for latest version of Selenium
https://github.com/mozilla/geckodriver/releases
brew install geckodriver

ChromeDriver for Selenium
https://sites.google.com/a/chromium.org/chromedriver/

brew install chromedriver


