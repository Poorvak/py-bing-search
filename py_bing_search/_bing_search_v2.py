"""BING API v5 requestor module."""
import json
import urllib
import httplib
import constants

headers = dict()


def search_bing(search_text,
                conn,
                offset=None,
                limit=None,
                market=None,
                safesearch=None,
                api_key=None):
    """Search bing method calls the BING Api for web results."""
    # Request headers
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
    params = urllib.urlencode(
        {
            'q': search_text,
            'count': limit,
            'offset': offset,
            'mkt': market,
            'safesearch': safesearch,
        }
    )
    try:
        conn.request(method='GET',
                     url='/api/v5/search/?{params}'.format(params=params),
                     body='{body}',
                     headers=headers)
        print req
        response = req.getresponse()
        data = response.read()
    except Exception as e:
        data = None
        print e
    return json.loads(data)
