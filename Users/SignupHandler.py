import MetaUser
import Redirect
import Hasher

def signup(RequestHandler):
  password = RequestHandler.request.get('password')
  email    = RequestHandler.request.get('email')
  redirect = RequestHandler.request.get('redirect')
  
  status = MetaUser.create(email, password)
  
  if status == MetaUser.SUCCESS:
    Redirect.go(RequestHandler, redirect, {'success':True})
  elif status == MetaUser.EMAIL_USED:
    Redirect.go(RequestHandler, redirect, {'success':False,'message':'Email address already in use'})