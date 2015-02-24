import LoginToken
import MetaUser
import Hasher
import Handlers
all = ['LoginToken', 'MetaUser', 'Hasher', 'Handlers']


# MAIN METHODS
def create_login_url(redirect_url):
  token = LoginToken.create()
  # NOTE. Never change the URL format without also changing the client.js expected URL format
  return 'users.login:%s:%s:%s' % (token.salt, token.token, redirect_url)


def create_signup_url(redirect_url):
  return 'users.signup:%s' % (redirect_url)


# HOOK HANDLER
import webapp2
class HookHandler(webapp2.RequestHandler):
  def get(self, url):
    from google.appengine.ext.webapp import template
    import os
    
    files = ['sha256.min.js', 'login_client.min.js', 'signup_client.min.js']
    joined_value = ''
    
    for file in files:
      path = os.path.join(os.path.dirname(__file__), 'scripts/%s' % file)
      joined_value += open(path, 'r').read()
    
    self.response.headers['Content-Type'] = 'application/javascript'
    self.response.out.write(joined_value)


# CONSTANTS
BASEURL = '/api/users'
HOOK = ('%s(?:/(.*))?' % BASEURL, HookHandler)