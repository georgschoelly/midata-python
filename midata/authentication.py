import requests

from midata import utils

sign_in_url = "/users/sign_in.json"

class AuthException(Exception):
    pass

class AuthInfo(object):
    def __init__(self, auth_json, server):
        self.server = server

        # grab authentication info
        try:
            user = auth_json['people'][0]
            self.token      = user['authentication_token']
            self.email      = user['email']
            self.last_login = utils.parse_midata_datetime(user['last_sign_in_at'])
            self.user_id    = user['id']
        except Exception as e:
            raise AuthException("Error parsing auth info.") from e

    def http_headers(self):
        return {
            'X-User-Email': self.email,
            'X-User-Token': self.token,
            'Accept':       'application/json',
        }

def sign_in(server, email, password):
    # check for https
    pass

    # http request
    auth_data = {
        'person[email]'   : email,
        'person[password]': password,
    }

    try:
        r = requests.post(server + sign_in_url, data=auth_data)
        auth_json = r.json()
    except Exception as e:
        raise AuthException("HTTP request failed")

    if r.status_code == 401:
        return None

    if r.status_code != 200:
        raise AuthException("Invalid status code: {}".format(r.status_code))

    # validate response
    try:
        if len(auth_json['people']) != 1:
            raise AuthException("Invalid number of people.")

        if auth_json['people'][0]['email'] != email:
            raise AuthException("Identity mismatch.")
    except Exception as e:
        if isinstance(e, AuthException):
            raise
        else:
            raise AuthException("Error trying to sign in.") from e

    return AuthInfo(auth_json, server)

def sign_out(auth_info):
    pass

def renew(auth_info):
    pass
