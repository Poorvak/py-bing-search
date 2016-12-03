"""Constants file for specifying all constants values."""

QUERY_BASE = "https://api.datamarket.azure.com/Bing/Search/{search_type}" \
    + "?Query={query}&$top={limit}&$skip={offset}&$format={format}&Adult='Off'&Market='en-IN'"

LIMIT = 10

OFFSET = 0

RETURN_FORMAT = 'json'

SAFE = False

MARKET = 'en-IN'

SAFESEARCH = 'Off'
