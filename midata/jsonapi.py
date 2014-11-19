class MidataObject(object):
    _field_name = None # overwrite in subclass
    id          = None # automatically extracted for every class

    def __init__(self, inner_json, full_json):
        self._inner_json = inner_json
        self._full_json  = full_json

        self.id = int(inner_json['id'])

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

