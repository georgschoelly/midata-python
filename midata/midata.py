import requests
import collections.abc
from midata import jsonapi

class Person(object):
    def __init__(self, json):
        assert len(json['people']) == 1
        self._raw   = json
        self._cache = jsonapi.Cache(json)

        self.person_id  = json['people'][0]['id']
        person_json     = self._cache['people'][self.person_id]

        self.first_name = person_json['first_name']
        self.last_name  = person_json['last_name']

    @property
    def roles(self):
        role_ids = {x for x in self._cache['people'][self.person_id]['links']['roles']}
        return [Role(self._cache['roles'][role_id]) for role_id in role_ids]

    @property
    def groups(self):
        group_ids = (role.group for role in self.roles)
        return [self._cache['groups'][group_id] for group_id in group_ids]

class Group(object):
    def __init__(self, json):
        assert len(json['groups']) == 1
        self._raw = json
        self._group_json = json['groups'][0]
        self.group_id = self._group_json['id']

    @property
    def children(self):
        return self._group_json['links'].get('children', [])

class Members(collections.abc.Sequence):
    def __init__(self, json):
        self._raw = json
        self._list = []
        self._cache = jsonapi.Cache(json)

        for person in json['people']:
            person_id = person['id']
            for role_id in person['links']['roles']:
                role = self._cache['roles'][role_id]
                self._list.append((Role(role), Person(person)))

    def __getitem__(self, index):
        return self._list[index]

    def __len__(self):
        return len(self._list)

class Role(object):
    def __init__(self, role_json):
        self._role_json  = role_json
        self.description = role_json['label'] or role_json['role_type']
        self.group       = role_json['links']['group']
        self.role_type   = role_json['role_type']

def get_person(auth_info, person_id):
    json = _fetch_content(auth_info, '/groups/1/people/{}'.format(person_id))
    return Person(json)

def get_group(auth_info, group_id):
    json = _fetch_content(auth_info, '/groups/{}'.format(group_id))
    return Group(json)

def get_members(auth_info, group_id):
    json = _fetch_content(auth_info, '/groups/{}/people'.format(group_id))
    return Members(json)

def _fetch_content(auth_info, url):
    r = requests.get(auth_info.server + url.format(auth_info.user_id),
                     headers=auth_info.http_headers())

    if r.status_code != 200:
        raise Exception("Error!")

    return r.json()

