import unittest
import HTMLTestRunner
import os
import time
from last_asset import LastAsset
from forward_thumbs import ForwardThumbs
from next_slates import NextSlates
from thumbs import Thumbs
from forward_back import ForwardBack
from platform_id import PlatformId
from video_complete import VideoComplete

# get the directory path to output report file
dir = os.getcwd()
 
# get all tests from SearchText and HomePageTest class
last_asset = unittest.TestLoader().loadTestsFromTestCase(LastAsset)
forward_thumbs = unittest.TestLoader().loadTestsFromTestCase(ForwardThumbs)
next_slates = unittest.TestLoader().loadTestsFromTestCase(NextSlates)
thumbs = unittest.TestLoader().loadTestsFromTestCase(Thumbs)
forward_back = unittest.TestLoader().loadTestsFromTestCase(ForwardBack)
video_complete = unittest.TestLoader().loadTestsFromTestCase(VideoComplete)
platform_id = unittest.TestLoader().loadTestsFromTestCase(PlatformId)
 
# create a test suite combining search_text and home_page_test
test_suite = unittest.TestSuite([forward_thumbs,next_slates,thumbs,forward_back,video_complete,platform_id])
 
# open the report file
outfile = open(dir + "/reports/TestSummary" + str(int(time.time())) + ".html", "w")
 
# configure HTMLTestRunner options
runner = HTMLTestRunner.HTMLTestRunner(stream=outfile,title='Test Report', description='Acceptance Tests')
 
# run the suite using HTMLTestRunner
runner.run(test_suite)