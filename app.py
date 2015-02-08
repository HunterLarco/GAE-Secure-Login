from google.appengine.ext.webapp import template
import webapp2
import os

import Users


class LoginHandler(Users.Handlers.LoginHandler):
  def post(self):
    self.response.out.write(self.was_success())
    self.response.out.write('<br/>'+str(self.error()))
    self.response.out.write('<br/>'+str(self.get_current_user()))
  
  def get(self):
    template_values = {
      'users_client': Users.BASEURL,
      'login_url': Users.create_login_url('/login')
    }
    path = os.path.join(os.path.dirname(__file__), 'login.html')
    self.response.out.write(template.render(path, template_values))


class SignupHandler(Users.Handlers.SignupHandler):
  def post(self):
    self.response.out.write(self.was_success())
    self.response.out.write('<br/>'+str(self.error()))
  
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
                ('/login/?', LoginHandler)
              ], debug=True)