import LoginToken
import Redirect
import MetaUser
import Hasher


# CONSTANTS
SUCCESS             = 'LH0'
INVALID_LOGIN_TOKEN = 'LH1'
USER_DOESNT_EXIST   = 'LH2'
INVALID_PASSWORD    = 'LH3'


def validate(RequestHandler):
  logintoken = RequestHandler.request.get('logintoken')
  password   = RequestHandler.request.get('password')
  email      = RequestHandler.request.get('email')
  
  token = LoginToken.get_by_token(logintoken)
  if token == None:
    return INVALID_LOGIN_TOKEN
  
  user = MetaUser.get_by_email(email)
  import logging
  logging.info(user)
  if user == None:
    return USER_DOESNT_EXIST
  
  user_password = token.use(user.password)
  
  logging.info(user_password)
  logging.info(password)
  
  if user_password != password:
    return INVALID_PASSWORD
  
  return SUCCESS


def login(RequestHandler):
  redirect = RequestHandler.request.get('redirect')
  
  status = validate(RequestHandler)
  default_error = {'success': False, 'message': 'Unknown Error'}
  
  Redirect.go(RequestHandler, redirect, {
    SUCCESS:             {'success': True},
    INVALID_LOGIN_TOKEN: {'success': False, 'message': 'Invalid Login Token'},
    USER_DOESNT_EXIST:   {'success': False, 'message': 'Password Email Combination Does Not Exist'},
    INVALID_PASSWORD:    {'success': False, 'message': 'Password Email Combination Does Not Exist'}
  }.get(status, default_error))