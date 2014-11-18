import requests
import collections.abc

class MidataObject(object):
    def __init__(self, inner_json, full_json):
        self._inner_json = inner_json
        self._full_json  = full_json

    @classmethod
    def extract_linked(cls, full_json):
        return cls._extract(full_json['linked'][cls._field_name], full_json)

    @classmethod
    def extract_primary(cls, full_json):
        return cls._extract(full_json[cls._field_name], full_json)

    @classmethod
    def _extract(cls, objects_json, full_json):
        objects = (cls(inner_json, full_json) for inner_json in objects_json)
        return objects

class Person(MidataObject):
    _field_name = 'people'

    def __init__(self, inner_json, full_json):
        super().__init__(inner_json, full_json)

        self.person_id  = inner_json['id']
        self.first_name = inner_json['first_name']
        self.last_name  = inner_json['last_name']

    @property
    def roles(self):
        role_ids = set(self._inner_json['links']['roles'])
        return (role for role in Role.extract_linked(self._full_json)
                     if role.role_id in role_ids)

class Group(MidataObject):
    _field_name = 'groups'

    def __init__(self, inner_json, full_json):
        super().__init__(inner_json, full_json)

        self.group_id   = inner_json['id']
        self.name       = inner_json['name']
        self.group_type = inner_json['group_type']

    @property
    def children(self):
        return self._inner_json['links'].get('children', [])

class Role(MidataObject):
    _field_name = 'roles'

    def __init__(self, inner_json, full_json):
        super().__init__(inner_json, full_json)

        self.role_id     = inner_json['id']
        self.description = inner_json['label'] or inner_json['role_type']
        self.role_type   = inner_json['role_type']

    # TODO cache all_groups
    @property
    def group(self):
        group_id = self._inner_json['links']['group']
        all_groups = Group.extract_linked(self._full_json)
        # extract first matching group
        return next(x for x in all_groups if x.group_id == group_id)

def get_person(auth_info, person_id):
    json = _fetch_content(auth_info, '/groups/1/people/{}'.format(person_id))
    people = list(Person.extract_primary(json))
    assert len(people) == 1
    return people[0]

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

