from google.appengine.ext import ndb


class LoginToken(ndb.Model):
  salt = ndb.StringProperty(indexed=False)
  creation_date = ndb.DateTimeProperty(auto_now_add=True, indexed=True)
  # TODO write cleanup program


class Token:
  def __init__(self, token=None):
    if token == None:
      token = LoginToken()
      token.salt = self.__createSalt__()
      token.put()
    
    self.__token__ = token
    self.salt = token.salt
    self.token = token.key.urlsafe()
  
  def __createSalt__(self, length=16):
    import random
    return ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for i in range(length))
  
  def use(self, password):
    import Hasher
    password = Hasher.sha256(password, salt=self.salt)
    self.__token__.key.delete()
    return password


def get_by_token(token):
  entity = ndb.Key(urlsafe=token).get()
  if entity == None:
    return None
  return Token(token=entity)


def create():
  return Token()