# params = {'lang':'en','tag':'python'}
def go(RequestHandler, url, params={}):
  import urllib
  import urlparse
  
  url_parts = list(urlparse.urlparse(url))
  query = dict(urlparse.parse_qsl(url_parts[4]))
  query.update(params)
  url_parts[4] = urllib.urlencode(query)
  
  RequestHandler.redirect(urlparse.urlunparse(url_parts))