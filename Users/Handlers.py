import webapp2
import MetaUser


class LoginHandler(webapp2.RequestHandler):
  
  __meta__ = None
  __error__ = None
  __success__ = False
  
  
  def login(self):
    import LoginToken
    import MetaUser
    
    logintoken = self.request.get('logintoken')
    password   = self.request.get('password')
    email      = self.request.get('email')
  
    token = LoginToken.get_by_token(logintoken)
    if token == None:
      self.__error__ = 'Invalid login token'
      return
  
    self.__meta__ = MetaUser.get_by_email(email)
    if self.__meta__ == None:
      self.__error__ = 'User does not exist'
      return
  
    user_password = token.use(self.__meta__.password)

    if user_password != password:
      self.__error__ = 'Invalid password'
      return
    
    self.__success__ = True
  
  
  def was_success(self):
    return self.__success__
  
  
  def error(self):
    if self.was_success():
      return None
    return 'Unknown Error' if self.__error__ == None else self.__error__
  
  
  def get_current_user(self):
    if not self.was_success() or self.__meta__.entity == None:
      return None
    return self.__meta__.entity.get()
  
  
  def dispatch(self):
    if self.request.method.lower() == 'post':
      self.__status__ = self.login()
    super(LoginHandler, self).dispatch()










class SignupHandler(webapp2.RequestHandler):
  
  __meta__ = None
  
  
  def signup(self):
    password = self.request.get('password')
    email    = self.request.get('email')
    
    if len(password) == 0 or len(email) == 0:
      raise Exception('Missing Sign Up Parameter')
  
    password = password[3:] + password[:3]
  
    self.__meta__ = MetaUser.create(email, password)
  
  
  def was_success(self):
    return isinstance(self.__meta__, MetaUser.MetaUser)
  
  
  def error(self):
    if self.was_success():
      return None
    return {
      MetaUser.INVALID_EMAIL : 'Invalid Email Address',
      MetaUser.EMAIL_USED    : 'Email Address Already Exists'
    }.get(self.__meta__, 'Unknown Error')
  
  
  def attach(self, user_entity):
    if not self.was_success():
      return False
    
    self.__meta__.entity = user_entity.key
    self.__meta__.put()
    
    return True
  
  
  def dispatch(self):
    if self.request.method.lower() == 'post':
      self.__status__ = self.signup()
    super(SignupHandler, self).dispatch()