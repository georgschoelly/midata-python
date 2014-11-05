#!/usr/bin/env python3

# import hack, such that the midata module is in the search path
import sys; import os.path
sys.path.append(os.path.realpath(os.path.join(__file__, "..", "..")))

import requests
import midata
from midata import authentication as auth

# input data
server   = "https://db.scout.ch"
email    = "user@server"
password = "*******"

# log in
auth_info = auth.sign_in(server, email, password)

if not auth_info:
    print("Unable to login.")
    exit()

# grab information about the logged-in user
user = midata.get_person(auth_info, auth_info.user_id)

print(user.first_name)
for group in user.groups:
    print("  {} {}".format(group['group_type'], group['name']))

