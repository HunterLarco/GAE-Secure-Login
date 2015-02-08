from google.appengine.ext.webapp import template
import webapp2
import os

import Users


class MainHandler(webapp2.RequestHandler):
  def get(self):
    template_values = {
      'users_client': Users.BASEURL,
      'login_url': Users.create_login_url('/login')
    }
    path = os.path.join(os.path.dirname(__file__), 'login.html')
    self.response.out.write(template.render(path, template_values))


class SignupHandler(webapp2.RequestHandler):
  def get(self):
    template_values = {
      'users_client': Users.BASEURL,
      'signup_url': Users.create_signup_url('/signup')
    }
    path = os.path.join(os.path.dirname(__file__), 'signup.html')
    self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication([
                Users.HOOK,
                ('/signup/?', SignupHandler),
                ('/.*', MainHandler)
              ], debug=True)