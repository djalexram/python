# iris-qa-automation
Robot Framework works with Python 2.x and 3.x but some of the libraries require Pyton 2.x.
https://iristv.atlassian.net/wiki/display/QD/QA+Robot+Automation+Setup
https://iristv.atlassian.net/wiki/display/QD/QA+Python+Automation

MAC OS SETUP

Install Apple Xcode and accept license
sudo xcodebuild -license accept

Install Homebrew
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Install updated Python which includes pip.
brew install python

PIP INSTALL
Installing with pip (you may have to install using sudo for some items)
pip install robotframework
pip install robotframework-selenium2library
pip install robotframework-httplibrary
pip install robotframework-pabot
pip install browsermob-proxy

Geckdriver is required for latest version of Selenium
https://github.com/mozilla/geckodriver/releases
cp geckodriver /usr/bin/

ChromeDriver for Selenium
https://sites.google.com/a/chromium.org/chromedriver/
cp chromedriver /usr/bin/

ROBOT RESOURCE VARIABLES
You can update the two arrays/lists with the URLs and player types. Following is for testing single player:
@{URLS} http://s3.amazonaws.com/iris-playground/cosmos/test_pages/brightcovenextgen.html http://s3.amazonaws.com/iris-playground/cosmos/test_pages/jwplayer.html http://www.kaltura.com/index.php/extwidget/preview/partner_id/1344571/uiconf_id/38056231/entry_id/0_42qi7rzj/embed/dynamic?&flashvars[streamerType]=auto

MULITPLAYER TESTING:
@{URLS_MULTI} http://s3.amazonaws.com/iris-playground/cosmos/test_pages/brightcovenextgen.html

HEADLESS SETUP
sudo apt-get install xvfb


ROBOT USAGE
ENTIRE SUITE
pybot regression -d reports -T -L DEBUG

Run all tests tagged as "2player"
pybot regression -i 2player -d reports -T -L DEBUG


SINGLE TEST
pybot regression/forward_thumbs.txt -d reports -T -L DEBUG


PABOT
Following command is to run same test parallel with a different browser:
ENTIRE SUITE
pabot --verbose --argumentfile1 arg1.txt --argumentfile2 arg2.txt --argumentfile3 arg3.txt -d reports -T -L DEBUG regression

SINGLE TEST
pabot --verbose --argumentfile1 arg1.txt --argumentfile2 arg2.txt --argumentfile3 arg3.txt -d reports -T -L DEBUG regression/forward_thumbs.txt

PYTHON AUTOMATION
Making use of both Selenium and Browsermob proxy we are now able to check individual requests within automated tests.
The proxy server JAR file is included with the automation code. For setup make sure to install a recent Java SDK.

BrowserMob Proxy
https://bmp.lightbody.net/

BROWSERMOB DOCUMENTATON
https://browsermob-proxy-py.readthedocs.io/en/stable/


ROBOT DOCUMENTATION
http://robotframework.org/robotframework/latest/libraries/BuiltIn.html
http://robotframework.org/robotframework/latest/libraries/String.html
http://robotframework.org/Selenium2Library/Selenium2Library.html
http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html
https://github.com/robotframework/robotframework/blob/master/doc/userguide/src/CreatingTestData/CreatingTestCases.rst

ROBOT COMMAND LINE PARAMETERS
https://robot-framework.readthedocs.io/en/2.9.2/_modules/robot/run.html
