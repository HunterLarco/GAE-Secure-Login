from google.appengine.ext import ndb


# CONSTANTS
SUCCESS = 'MU0'
INVALID_EMAIL = 'MU1'
EMAIL_USED = 'MU2'


class MetaUser(ndb.Model):
  email = ndb.StringProperty(indexed=True)
  password = ndb.StringProperty(indexed=False)


def get_by_email(email):
  return MetaUser.query(MetaUser.email == email).get()


def create(email, password):
  if get_by_email(email) != None:
    return EMAIL_USED
  
  user = MetaUser()
  user.email = email
  user.password = password
  user.put()
  
  return SUCCESS