import json
import random
import string
import hmac
import base64
import hashlib
import time
import requests

"""
Replace base_url, access_key and secret key 
accordingly (sandbox vs production)
"""
base_url = 'https://sandboxapi.rapyd.net'
secret_key = '<secret key>'
access_key = '<access key>'

"""
Generates and returns a unique random salt.
"""


def generate_salt(length=12):
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


"""
Returns the current time in seconds.
"""


def get_unix_time(days=0, hours=0, minutes=0, seconds=0):
    return int(time.time())


"""
Generates a signature in relation to, the random salt, current time, http
method, path, the request body and the app keys.
"""


def update_timestamp_salt_sig(http_method, path, body):
    if path.startswith('http'):
        path = path[path.find(f'/v1'):]
    salt = generate_salt()
    timestamp = get_unix_time()
    to_sign = (http_method, path, salt, str(timestamp), access_key, secret_key, body)

    h = hmac.new(secret_key.encode('utf-8'), ''.join(to_sign).encode('utf-8'), hashlib.sha256)
    signature = base64.urlsafe_b64encode(str.encode(h.hexdigest()))
    return salt, timestamp, signature


"""
The current header signature dictionary.
"""


def current_sig_headers(salt, timestamp, signature):
    sig_headers = {'access_key': access_key,
                   'salt': salt,
                   'timestamp': str(timestamp),
                   'signature': signature,
                   'idempotency': str(get_unix_time()) + salt}
    return sig_headers


"""
Formats the request body and returns it, and the unique salt, signature and current timestamp.
"""


def pre_call(http_method, path, body=None):
    str_body = json.dumps(body, separators=(',', ':'), ensure_ascii=False) if body else ''
    salt, timestamp, signature = update_timestamp_salt_sig(http_method=http_method, path=path, body=str_body)
    return str_body.encode('utf-8'), salt, timestamp, signature


"""
Creates the body and headers with the right signature according to the current request contexts,
for use in the make_request method.
"""


def create_headers(http_method, url, body=None):
    body, salt, timestamp, signature = pre_call(http_method=http_method, path=url, body=body)
    return body, current_sig_headers(salt, timestamp, signature)


"""
Reusable utility method.
Use this from anywhere in your application.
"""


def make_request(method, path, body=''):
    body, headers = create_headers(method, base_url + path, body)

    if method == 'get':
        response = requests.get(base_url + path, headers=headers)
    elif method == 'put':
        response = requests.put(base_url + path, data=body, headers=headers)
    elif method == 'delete':
        response = requests.delete(base_url + path, data=body, headers=headers)
    else:
        response = requests.post(base_url + path, data=body, headers=headers)

    if response.status_code != 200:
        raise TypeError(response, method, base_url + path)
    return json.loads(response.content)
