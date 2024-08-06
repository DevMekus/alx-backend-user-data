#!/usr/bin/env python3
"""Base module.
"""
import json
import uuid
from os import path
from datetime import datetime
from typing import TypeVar, List, Iterable


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA = {}


class Base():
    """Base class.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a Base instance.
        """
        sClass = str(self.__class__.__name__)
        if DATA.get(sClass) is None:
            DATA[sClass] = {}

        self.id = kwargs.get('id', str(uuid.uuid4()))
        if kwargs.get('created_at') is not None:
            self.created_at = datetime.strptime(kwargs.get('created_at'),
                                                TIMESTAMP_FORMAT)
        else:
            self.created_at = datetime.utcnow()
        if kwargs.get('updated_at') is not None:
            self.updated_at = datetime.strptime(kwargs.get('updated_at'),
                                                TIMESTAMP_FORMAT)
        else:
            self.updated_at = datetime.utcnow()

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """Modeule checks Equality.
        """
        if type(self) != type(other):
            return False
        if not isinstance(self, Base):
            return False
        return (self.id == other.id)

    def to_json(self, for_serialization: bool = False) -> dict:
        """Module Convert the object a JSON dictionary.
        """
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key[0] == '_':
                continue
            if type(value) is datetime:
                result[key] = value.strftime(TIMESTAMP_FORMAT)
            else:
                result[key] = value
        return result

    @classmethod
    def load_from_file(cls):
        """Module Load all objects from file.
        """
        sClass = cls.__name__
        file_path = ".db_{}.json".format(sClass)
        DATA[sClass] = {}
        if not path.exists(file_path):
            return

        with open(file_path, 'r') as f:
            objs_json = json.load(f)
            for obj_id, obj_json in objs_json.items():
                DATA[sClass][obj_id] = cls(**obj_json)

    @classmethod
    def save_to_file(cls):
        """Module Save all objects to file.
        """
        sClass = cls.__name__
        filePath = ".db_{}.json".format(sClass)
        jsonObject = {}
        for obj_id, obj in DATA[sClass].items():
            jsonObject[obj_id] = obj.to_json(True)

        with open(filePath, 'w') as f:
            json.dump(jsonObject, f)

    def save(self):
        """Module Save current object.
        """
        sClass = self.__class__.__name__
        self.updated_at = datetime.utcnow()
        DATA[sClass][self.id] = self
        self.__class__.save_to_file()

    def remove(self):
        """Module Remove object.
        """
        sClass = self.__class__.__name__
        if DATA[sClass].get(self.id) is not None:
            del DATA[sClass][self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """Module Count all objects.
        """
        sClass = cls.__name__
        return len(DATA[sClass].keys())

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """Return all objects.
        """
        return cls.search()

    @classmethod
    def get(cls, id: str) -> TypeVar('Base'):
        """Module Return one object by ID.
        """
        sClass = cls.__name__
        return DATA[sClass].get(id)

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """Search all objects with matching attributes.
        """
        sClass = cls.__name__
        def _search(obj):
            if len(attributes) == 0:
                return True
            for k, v in attributes.items():
                if (getattr(obj, k) != v):
                    return False
            return True

        return list(filter(_search, DATA[sClass].values()))