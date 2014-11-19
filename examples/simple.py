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

print("Logged in as:", end=" ")
print(user.first_name)

print("\nMember of the following groups:")
for role in user.roles:
    group = role.group
    print("  {} in {} {}".format(role.description, group.group_type, group.name))

# print members of first group
print("\nThe first group contains the following people:")
group_id = list(user.roles)[0].group.id
members = midata.get_members(auth_info, group_id)
for member in members:
    print("  {}".format(member))

# print first group's children
print("\nthe group has the following subgroups:")
group = midata.get_group(auth_info, group_id)
print(list(group.children))
