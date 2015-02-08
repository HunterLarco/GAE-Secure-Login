import LoginToken
import LoginHandler
import MetaUser
import Hasher
import SignupHandler
import Redirect
all = ['LoginToken', 'LoginHandler', 'MetaUser', 'Hasher', 'SignupHandler', 'Redirect']


# MAIN METHODS
def create_login_url(redirect_url):
  token = LoginToken.create()
  # NOTE. Never change the URL format without also changing the client.js expected URL format
  from urllib import quote
  return '%s/login/%s/%s?redirect=%s' % (BASEURL, token.salt, token.token, quote(redirect_url))


def create_signup_url(redirect_url):
  from urllib import quote
  return '%s/signup?redirect=%s' % (BASEURL, quote(redirect_url))


# HOOK HANDLER
import webapp2
class HookHandler(webapp2.RequestHandler):
  
  def signup(self):
    SignupHandler.signup(self)
  
  def login(self):
    LoginHandler.login(self)
  
  def post(self, url):
    url = url.split('/')
    if url[0] == 'login' and len(url) == 1:
      self.login()
    elif url[0] == 'signup' and len(url) == 1:
      self.signup()
    else:
      self.error(404)
      self.response.out.write('Error 404')
  
  def get(self, url):
    from google.appengine.ext.webapp import template
    import os
    
    files = ['sha256.min.js', 'login_client.min.js', 'signup_client.min.js']
    joined_value = ''
    template_values = {
      'BASEURL': BASEURL
    }
    
    for file in files:
      path = os.path.join(os.path.dirname(__file__), 'scripts/%s' % file)
      joined_value += template.render(path, template_values)
    
    self.response.headers['Content-Type'] = 'application/javascript'
    self.response.out.write(joined_value)


# CONSTANTS
BASEURL = '/api/users'
HOOK = ('%s(?:/(.*))?' % BASEURL, HookHandler)