"""
Py Bin Search main class.

This code is a fork and is improved over the repo
"https://github.com/tristantao/py-bing-search.git"
"""
import httplib
import urllib2
import requests
import constants
import _bing_search_v2


class PyBingException(Exception):
    """PyBingException is the base class for Exception Handling."""

    pass


class PyBingSearch(object):
    """Parent class for the individual search."""

    def __init__(self, api_key, query, query_base, version=None):
        """
        Constructor method.

        Takes in the API_KEY and checks for pagination
        Arguments:
        ----------------
        api_key : Generated from BING Console
        query: search_text
        query_base: API end-point

        """
        if not version:
            version = 1
        self.api_key = api_key
        self.offset = constants.OFFSET
        self.query = query
        self.QUERY_URL = query_base
        self.version = version

    def search(self, limit=None,
               offset=None, return_format=None,
               version=None):
        """Return the result list, and also the uri for next page."""
        if not limit:
            limit = constants.LIMIT
        if not offset:
            offset = constants.OFFSET
        if not return_format:
            return_format = constants.RETURN_FORMAT
        if not version:
            version = self.version
        return self._search(limit=limit,
                            offset=offset,
                            format=return_format,
                            version=version)

    # def search_all(self, limit=None, return_format=None):
    #     """Return a single list containing up to 'limit' Result objects."""
    #     if not limit:
    #         limit = constants.LIMIT
    #     desired_limit = limit
    #     results = self._search(limit=limit, format=return_format)
    #     result_length = len(results)
    #     while result_length < desired_limit:
    #         limit = limit - result_length
    #         more_results = self._search(limit=limit, format=return_format)
    #         if not more_results:
    #             break
    #         results += more_results
    #         limit = limit - len(more_results)
    #     return results


class PyBingWebException(Exception):
    """Inherit PyBinException Base class."""

    pass


class PyBingWebSearch(PyBingSearch):
    """Web Search Class."""

    WEB_QUERY_BASE = constants.QUERY_BASE

    def __init__(self,
                 query,
                 api_key,
                 version=None):
        """Default Constructor for making object for api_key."""
        if not version:
            version = 1
        PyBingSearch.__init__(self,
                              api_key=api_key,
                              query=query,
                              query_base=self.WEB_QUERY_BASE,
                              version=version)

    def _search(self,
                limit=None,
                offset=None,
                format=None,
                version=None):
        """Return a list of result objects."""
        if not limit:
            limit = constants.LIMIT
        if not format:
            format = constants.RETURN_FORMAT
        if not offset:
            offset = constants.OFFSET
        if not version:
            version = self.version
        if version == 1:
            url = self.QUERY_URL.format(
                search_type='Web',
                query=urllib2.quote(
                    "'{}'".format(self.query)),
                limit=limit,
                offset=offset,
                format='json')
            # Need to find the optimal procedure for this
            res = requests.get(url, auth=("", self.api_key))
            try:
                json_results = res.json()
            except ValueError:
                raise PyBingWebException("[Error] Code:%s, Error:%s" % (
                    res.status_code,
                    res.text))
        if version == 2:
            json_results = _bing_search_v2.search_api_v2_dict(search_text=self.query,
                                                              api_key=self.api_key,
                                                              offset=offset,
                                                              limit=limit)
        print json_results
        json_results = json_results.get('d', list())
        if json_results:
            json_results = json_results.get('results', list())
        packaged_results = list()
        packaged_results = [make_dict(result=single_result_json)
                            for single_result_json in json_results]
        return packaged_results


def make_dict(result):
    """Converting result to dict."""
    response = dict()
    response.update(
        {
            'url': result.get('Url', None),
            'title': result.get('Title', None),
            'description': result.get('Description', None),
            'card_type': 1,
            'icon_url': None,
            'provider_icon_url': None,
            'action_type': 1,
        })
    return response


class WebResult(object):
    """
    The class represents a SINGLE search result.

    Each result will come with the following:

    #For the actual results#
    title: title of the result
    url: the url of the result
    id: the id of the bing page
    description: description for the result
    """

    def __init__(self,
                 result):
        """Default Constructor."""
        self.url = result['Url']
        self.title = result['Title']
        self.description = result['Description']
        self.id = result['ID']


class PyBingImageException(Exception):
    """Image Exception Handling."""

    pass


class PyBingImageSearch(PyBingSearch):
    """Image search for BING Api."""

    IMAGE_QUERY_BASE = constants.QUERY_BASE

    def __init__(self,
                 api_key,
                 query):
        """Default Constructor."""
        PyBingSearch.__init__(self,
                              api_key=api_key,
                              query=query,
                              query_base=self.IMAGE_QUERY_BASE)

    def _search(self,
                limit=None,
                offset=None,
                format=None):
        """Return a list of result objects."""
        if not limit:
            limit = constants.LIMIT
        if not format:
            format = constants.RETURN_FORMAT
        if not offset:
            offset = constants.OFFSET
        url = self.QUERY_URL.format(
            search_type='Image',
            query=urllib2.quote(
                "'{}'".format(self.query)),
            limit=limit,
            offset=offset,
            format=format)
        res = requests.get(url, auth=("", self.api_key))
        try:
            json_results = res.json()
        except ValueError:
            raise PyBingImageException("Code:%s, Error: %s" % (res.status_code,
                                                               res.text))
        json_results = json_results.get('d', None)
        if json_results:
            json_results = json_results.get('results', None)
        packaged_results = [ImageResult(single_result_json)
                            for single_result_json in json_results]
        self.offset += len(packaged_results)
        return packaged_results


class ImageResult(object):
    """
    The class represents a single image search result.

    Each result will come with the following:

    #For the actual image results#
    self.id: id of the result
    self.title: title of the resulting image
    self.media_url: url to the full size image
    self.source_url: url of the website that contains the source image
    self.width: width of the image
    self.height: height of the image
    self.file_size: size of the image (in bytes) if available
    self.content_type the MIME type of the image if available
    self.meta: meta info
    """

    def __init__(self, result):
        """Default Constructor."""
        self.id = result['ID']
        self.title = result['Title']
        self.media_url = result['MediaUrl']
        self.source_url = result['SourceUrl']
        self.display_url = result['DisplayUrl']
        self.width = result['Width']
        self.height = result['Height']
        self.file_size = result['FileSize']
        self.content_type = result['ContentType']
        self.meta = self._Meta(result['__metadata'])


class PyBingVideoException(Exception):
    """Video Exception."""

    pass


class PyBingVideoSearch(PyBingSearch):
    """Video Search Class."""

    VIDEO_QUERY_BASE = constants.QUERY_BASE

    def __init__(self, api_key, query):
        """Default Constructor."""
        PyBingSearch.__init__(self,
                              api_key=api_key,
                              query=query,
                              query_base=self.VIDEO_QUERY_BASE)

    def _search(self,
                limit=None,
                offset=None,
                format=None):
        """Return a list of result objects."""
        if not limit:
            limit = constants.LIMIT
        if not format:
            format = constants.RETURN_FORMAT
        if not offset:
            offset = constants.OFFSET
        url = self.QUERY_URL.format(
            search_type='Video',
            query=urllib2.quote(
                "'{}'".format(self.query)),
            limit=limit,
            offset=offset,
            format=format)
        res = requests.get(url, auth=("", self.api_key))
        try:
            json_results = res.json()
        except ValueError:
            raise PyBingVideoException("Code:%s, Error: %s" % (res.status_code,
                                                               res.text))
        json_results = json_results.get('d', None)
        if json_results:
            json_results = json_results.get('results', None)
        packaged_results = [VideoResult(single_result_json)
                            for single_result_json in json_results]
        self.offset += len(packaged_results)
        return packaged_results


class VideoResult(object):
    """
    The class represents a single Video search result.

    Each result will come with the following:

    #For the actual Video results#
    self.id: id of the result
    self.title: title of the resulting Video
    self.media_url: url to the full size Video
    self.display_url: url to display on the search result.
    self.run_time: run time of the video
    self.meta: meta info

    #Meta info#:
    meta.uri: the search uri for bing
    meta.type: for the most part VideoResult
    """

    def __init__(self, result):
        """Default Constrictor."""
        self.id = result['ID']
        self.title = result['Title']
        self.media_url = result['MediaUrl']
        self.display_url = result['DisplayUrl']
        self.run_time = result['RunTime']
        self.meta = self._Meta(result['__metadata'])


class PyBingNewsException(Exception):
    """News Exception."""

    pass


class PyBingNewsSearch(PyBingSearch):
    """News Search Class."""

    NEWS_QUERY_BASE = constants.QUERY_BASE

    def __init__(self, api_key, query):
        """Default Constructor."""
        PyBingSearch.__init__(self,
                              api_key=api_key,
                              query=query,
                              query_base=self.NEWS_QUERY_BASE)

    def _search(self,
                limit=None,
                offset=None,
                format=None):
        """Return a list of result objects."""
        if not limit:
            limit = constants.LIMIT
        if not format:
            format = constants.RETURN_FORMAT
        if not offset:
            offset = constants.OFFSET
        url = self.QUERY_URL.format(
            search_type='Video',
            query=urllib2.quote(
                "'{}'".format(self.query)),
            limit=limit,
            offset=offset,
            format=format)
        res = requests.get(url, auth=("", self.api_key))
        try:
            json_results = res.json()
        except ValueError:
            raise PyBingNewsException("Code:%s, Error: %s" % (res.status_code,
                                                              res.text))
        json_results = json_results.get('d', None)
        if json_results:
            json_results = json_results.get('results', None)
        packaged_results = [NewsResult(single_result_json)
                            for single_result_json in json_results]
        self.offset += len(packaged_results)
        return packaged_results


class NewsResult(object):
    """
    The class represents a single News search result.

    Each result will come with the following:

    #For the actual News results#
    self.id: id of the result
    self.title: title of the resulting News
    self.url: url to the News
    self.description: description of the article
    self.date: date of the News
    self.meta: meta info
    """

    def __init__(self, result):
        """Default Constructor."""
        self.id = result['ID']
        self.title = result['Title']
        self.url = result['Url']
        self.source = result['Source']
        self.description = result['Description']
        self.date = result['Date']
        self.meta = self._Meta(result['__metadata'])

if __name__ == '__main__':
    py_bing_object = PyBingWebSearch(api_key=constants.API_KEY,
                                     query='sex')
    print py_bing_object.search(offset=0,
                                limit=10,
                                return_format='json')
