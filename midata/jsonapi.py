import itertools
from copy import copy
from collections import defaultdict
import collections.abc


_special_top_level_keys = {'linked', 'links', 'meta', 'data'}

class Cache(collections.abc.Mapping):

    def __init__(self, data=None):
        self._object_cache = defaultdict(dict)

        if object:
            self.add_data(data)

    def __len__(self):
        return len(self._object_cache)

    def __iter__(self):
        return iter(self._object_cache)

    def __getitem__(self, key):
        return self._object_cache[key]

    def add_data(self, data_tree, top_type='data'):
        object_lists = []

        # the 'main' data can be either under the 'data' key or its type
        if top_type == 'data' and 'data' not in data_tree:
            names = set(data_tree.keys()) - _special_top_level_keys
            if len(names) != 1:
                raise Exception("Unable to figure out top-level data type.")

            top_type = names.pop()
            
        object_lists.append((top_type, data_tree[top_type]))

        # get linked items
        if 'linked' in data_tree:
            for (k,v) in data_tree['linked'].items():
                object_lists.append((k, v))

        # add items to cache
        for type, objs in object_lists:
            for obj in objs:
                if not obj['id'] in self[type]:
                    self[type][obj['id']] = copy(obj)
                else:
                    old = self[type][obj['id']]
                    old.update(obj)

