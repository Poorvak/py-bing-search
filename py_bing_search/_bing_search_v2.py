"""BING API v5 requestor module."""
import json
import urllib
import urlparse
import requests
import constants

session = requests.session()

def search_bing(search_text,
                api_key,
                offset=None,
                limit=None,
                market=None,
                safesearch=None):
    """Search bing method calls the BING Api for web results."""
    # Request headers
    headers = dict()
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
        req = session.get(url="https://api.cognitive.microsoft.com/bing/v5.0/search",
                          params=params,
                          headers=headers)
        return_resp = req.json()
    except Exception:
        return_resp = dict()
    return return_resp


def make_dict(item):
    """Dictionary parser."""
    resp = dict()
    resp["Description"] = item.get("snippet", None)
    resp["Title"] = item.get("name", None)
    resp["Url"] = item.get("url", None)
    if resp.get("Url"):
        parsed = urlparse.urlparse(resp["Url"])
        params = urlparse.parse_qsl(parsed.query)
        for key, value in params:
            if key == 'r':
                resp.update({"Url": value})
    return resp


def search_api_v2_dict(search_text,
                       api_key,
                       offset=None,
                       limit=None,
                       market=None,
                       safesearch=None):
    """This method for search_api_v2 for making the response structure similar to v1."""
    resp = search_bing(search_text=search_text,
                       offset=offset,
                       limit=limit,
                       market=market,
                       safesearch=safesearch,
                       api_key=api_key)
    resp = resp.get("webPages", dict()).get("value", list())
    return dict(d=dict(results=[make_dict(item=item) for item in resp]))


if __name__ == '__main__':
    search_bing(search_text='bing search',
                conn=httplib.HTTPSConnection('api.cognitive.microsoft.com'))

