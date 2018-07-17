import pytest
import requests  

import ast
import json
import sys

@pytest.mark.watchcall
class TestWatchCall(object):

	def test_watch_call(self,watch_call):
		print watch_call + "\n"
		temp = requests.get(watch_call)
		print temp.text
		assert "Sclera" not in temp.text, "ALERT DevOps, Sclera error"
		assert '"sc":true' in temp.text, "ALERT DevOps, Incorrect response for USA, sc:false"
		print "\nHTTP status code: " + str(temp.status_code)
		temp.raise_for_status()