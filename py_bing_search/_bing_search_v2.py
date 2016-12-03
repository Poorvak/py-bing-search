"""BING API v5 requestor module."""
import ast
import json
import urllib
import httplib
import constants

conn=httplib.HTTPSConnection('api.cognitive.microsoft.com')


def search_bing(search_text,
                offset=None,
                limit=None,
                market=None,
                safesearch=None,
                api_key=None):
    """Search bing method calls the BING Api for web results."""
    # Request headers
    global conn
    headers = dict()
    if not api_key:
        api_key = constants.NEW_BING_API_KEY
    headers["Ocp-Apim-Subscription-Key"] = api_key

    if not limit:
        limit = constants.LIMIT

    if not offset:
        offset = constants.OFFSET

    if not market:
        market = constants.MARKET

    if not safesearch:
        safesearch = constants.SAFESEARCH

    # Request parameters
    params = urllib.urlencode(dict(q=search_text, count=limit,
                                   offset=offset, mkt=market, safesearch=safesearch))
    try:
        conn.request(method='GET',
                     url='/bing/v5.0/search?%s' % params,
                     body='{body}',
                     headers=headers)
        response = conn.getresponse()
        data = json.dumps(response.read())
        try:
            return_resp = json.loads(data)
        except ValueError:
            return_resp = dict()
    except Exception:
        pass
    return return_resp


def make_dict(item):
    """Dictionary parser."""
    resp = dict()
    resp["Description"] = item.get("snippet", None)
    resp["Title"] = item.get("name", None)
    resp["Url"] = item.get("url", None)
    return resp


def search_api_v2_dict(search_text,
                       offset=None,
                       limit=None,
                       market=None,
                       safesearch=None,
                       api_key=None):
    """This method for search_api_v2 for making the response structure similar to v1."""
    resp = search_bing(search_text=search_text,
                       offset=offset,
                       limit=limit,
                       market=market,
                       safesearch=safesearch,
                       api_key=api_key)
    resp = json.loads(resp)
    resp = resp.get("webPages", dict()).get("value", list())
    return dict(d=dict(results=[make_dict(item=item) for item in resp]))


if __name__ == '__main__':
    search_bing(search_text='bing search',
                conn=httplib.HTTPSConnection('api.cognitive.microsoft.com'))

