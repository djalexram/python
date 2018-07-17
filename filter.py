import json

class Harfilter:
    def __init__(self,har):
        self.har = har


    def test_match(self, url, criterions=[], har=None):
        """
        Returns True if a request with given url and matching given criterions has been captured.
        :param url: URL substring the request URL has to contain
        :param criterions: List of criterions dicionaries the request has to match. Each dictionary has two items:
            "key" - dot separated path to the value in the HAR JSON we want to test. , i.e. "response.status", "request.headers" etc.
                See the examples/har.json to see how one single request is stored in the HAR format.
            "value" - desired value. Can be string, integer or dict.
        :param har: HAR JSON to search through. If not provided the proxy is asked to provide the actual one.
        """
        return len(self.get_matches(url, criterions, har)) != 0

    def get_matches(self, url,  har=None, criterions=[]):
        """
        Returns list of matching requests.
        :param url: URL substring the request URL has to contain
        :param criterions: List of criterions dicionaries the request has to match. Each dictionary has two items:
            "key" - dot separated path to the value in the HAR JSON we want to test. , i.e. "response.status", "request.headers" etc.
                See the examples/har.json to see how one single request is stored in the HAR format.
            "value" - desired value. Can be string, integer or dict.
        :param har: HAR JSON to search through. If not provided the proxy is asked to provide the actual one.
        """
        url_matches = self._filter_entries_by_url(url, har)
        if len(criterions):
            matches = []
            criterions_length = len(criterions)-1
            for entry in url_matches:
                for i, criterion in enumerate(criterions):
                    try:
                        if not self._test_entry_to_criterion_match(entry, criterion):
                            break
                    except:
                        return []
                else:
                    if i == criterions_length:
                        # all criterions match -> passed
                        matches.append(entry)
                    continue
        else:
            return url_matches
        return matches

    def _filter_entries_by_url(self, url, har):
        """
        Filters all captured requests by passed URL substring
        :param url: URL substring the request URL has to contain
        """
        if not har:
            har = self.har
        
        matches = []
        for entry in har["log"]["entries"]:
            if url in entry["request"]["url"]:
                matches.append(entry)
        return matches

    def _filter_return_url(self, url, har=None):
        """
        Filters all captured requests by passed URL substring
        :param url: URL substring the request URL has to contain
        """
        if not har:
            har = self.har
        
        matches = []
        for entry in har["log"]["entries"]:
            if url in entry["request"]["url"]:
                temp = entry["request"]["url"].encode('ascii', 'ignore')
                matches.append(temp)
        return matches

    def _filter_return_url_from_list(self, paths, har=None):
        """
        Filters all captured requests by passed URL substring
        :param url: URL substring the request URL has to contain
        """
        if not har:
            har = self.har
        
        matches = []
        for entry in har["log"]["entries"]:
            for path in paths:
                if path in entry["request"]["url"]:
                    temp = entry["request"]["url"].encode('ascii', 'ignore')
                    matches.append(temp)
        return matches


    def _filter_return_errors(self, url, har=None):
        """
        Filters all captured requests by passed URL substring
        :param url: URL substring the request URL has to contain
        """
        if not har:
            har = self.har
        
        matches = []
        for entry in har["log"]["entries"]:
            temp = entry["request"]["url"].encode('ascii', 'ignore')
            if url in entry["request"]["url"] and temp not in matches and entry["response"]["status"] >= 400:
                print "\nRequest failed w/ " + str(entry["response"]["status"]) + " error:\n" + entry["request"]["url"]
                if entry["response"]["content"].get("text"):
                    print "RESPONSE: " + str(entry["response"]["content"]["text"].encode('ascii', 'ignore'))
                temp = entry["request"]["url"].encode('ascii', 'ignore')
                matches.append(temp)
        return matches

    def _filter_return_errors_list(self, url, har=None):
        """
        Filters all captured requests by passed URL substring
        :param url: URL substring the request URL has to contain
        """
        if not har:
            har = self.har
        
        matches = []
        for entry in har["log"]["entries"]:
            temp = entry["request"]["url"].encode('ascii', 'ignore')
            if url in entry["request"]["url"] and temp not in matches and entry["response"]["status"] >= 400:
                print "\nRequest failed w/ " + str(entry["response"]["status"]) + " error:\n" + entry["request"]["url"]
                if entry["response"]["content"].get("text"):
                    print "RESPONSE: " + str(entry["response"]["content"]["text"].encode('ascii', 'ignore'))
                temp = entry["request"]["url"].encode('ascii', 'ignore')
                matches.append([temp,entry["response"]["content"].get("text","")])
        return matches

    def _filter_return_request_querystring(self, url, har=None):
        """
        Filters all captured requests by passed URL substring
        :param url: URL substring the request URL has to contain
        """
        if not har:
            har = self.har
        
        matches = []
        for entry in har["log"]["entries"]:
            if url in entry["request"]["url"]:
                temp = entry["request"]["queryString"]
                tempObject = {}
                for item in temp:
                    item = json.dumps(item, ensure_ascii=True)
                    json1 = json.loads(item)
                    key = json1['name']
                    val = json1['value']
                    tempObject[key]=val
                tempObject['url'] = entry["request"]["url"]
                tempObject['startedDateTime'] = entry["startedDateTime"]
                matches.append(tempObject)
        return matches


    def _filter_entries_by_url_response(self, url, har=None):
        """
        Filters all captured requests by passed URL substring
        :param url: URL substring the request URL has to contain
        """
        if not har:
            har = self.har
        
        matches = []
        if len(har["log"]["entries"]) > 1:
            for entry in har["log"]["entries"]:
                if url in entry["request"]["url"]:
                    if entry["response"]["status"] == 200 and entry["response"]["content"].get("text") and entry["response"]["content"]["text"] != "":
                        temp = entry["response"]["content"]["text"].encode('ascii', 'ignore')
                        matches.append(temp)
            return matches

    def _filter_entries_by_response(self, urls, har=None):
        """
        Filters all captured requests by passed URL substring
        :param url: URL substring the request URL has to contain
        """
        if not har:
            har = self.har
        
        matches = []
        if len(har["log"]["entries"]) > 1:
            for entry in har["log"]["entries"]:
                for url in urls:
                    if url in entry["request"]["url"]:
                        tempObject = {}
                        if entry["response"]["status"] == 200 and entry["response"]["content"].get("text") and entry["response"]["content"]["text"] != "":
                            tempObject['url'] = entry["request"]["url"]
                            tempObject['response'] = entry["response"]["content"]["text"].encode('ascii', 'ignore')
                            matches.append(tempObject)
            return matches

    def _test_entry_to_criterion_match(self, entry, criterion):
        """
        Tests single entry in HAR file whether it match given single criterion
        :param entry: Request entry from HAR JSON
        :param criterion:
        """
        parent = self._get_parent_node(entry, criterion["key"])
        parent_type = type(parent)
        if parent_type == list:
            unicriterions = { k.decode('utf8', "replace"): v.decode('utf8', "replace") for k, v in criterion["value"].items() }
            for item in parent:
                if set(unicriterions.items()) <= set({ k: v for k, v in item.items() }.items()):
                    return True
            return False
        if parent_type == str or int:
            return str(parent) == str(criterion["value"])

    def _get_parent_node(self, entry, key):
        """
        Finds item in single request entry matching given criterion key
        """
        parent = entry
        keys = key.split(".")
        for k in keys:
            try:
                parent = parent[k]
            except:
                raise Exception("key \"" + key + "\" was not found in HAR file")
        return parent