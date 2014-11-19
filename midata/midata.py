from midata.jsonapi import MidataObject
import requests
import collections.abc

class Person(MidataObject):
    _field_name = 'people'

    def __init__(self, inner_json, full_json):
        super().__init__(inner_json, full_json)

        self.first_name = inner_json['first_name']
        self.last_name  = inner_json['last_name']

    @property
    def roles(self):
        role_ids = set(int(x) for x in self._inner_json['links']['roles'])
        return (role for role in Role.extract_linked(self._full_json)
                     if role.id in role_ids)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

class Group(MidataObject):
    _field_name = 'groups'

    def __init__(self, inner_json, full_json):
        super().__init__(inner_json, full_json)

        self.name       = inner_json['name']
        self.group_type = inner_json['group_type']

    @property
    def children(self):
        return (int(x) for x in self._inner_json['links'].get('children', []))

class Role(MidataObject):
    _field_name = 'roles'

    def __init__(self, inner_json, full_json):
        super().__init__(inner_json, full_json)

        self.description = inner_json['label'] or inner_json['role_type']
        self.role_type   = inner_json['role_type']

    # TODO cache all_groups
    @property
    def group(self):
        group_id   = int(self._inner_json['links']['group'])
        all_groups = Group.extract_linked(self._full_json)
        # extract first matching group
        return next(x for x in all_groups if x.id == group_id)

def get_person(auth_info, person_id):
    json = _fetch_content(auth_info, '/groups/1/people/{}'.format(person_id))
    people = list(Person.extract_primary(json))
    assert len(people) == 1
    return people[0]

def get_group(auth_info, group_id):
    json = _fetch_content(auth_info, '/groups/{}'.format(group_id))
    groups = list(Group.extract_primary(json))
    assert len(groups) == 1
    return groups[0]

def get_members(auth_info, group_id):
    json = _fetch_content(auth_info, '/groups/{}/people'.format(group_id))
    return Person.extract_primary(json)

def _fetch_content(auth_info, url):
    r = requests.get(auth_info.server + url.format(auth_info.user_id),
                     headers=auth_info.http_headers())

    if r.status_code != 200:
        raise Exception("Error!")

    return r.json()

