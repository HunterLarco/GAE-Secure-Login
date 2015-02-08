def sha256(string, salt=''):
  from hashlib import sha256
  return sha256(salt+string).hexdigest()