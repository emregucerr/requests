# -*- coding: utf-8 -*-

"""
requests.structures
~~~~~~~~~~~~~~~~~~~

Data structures that power Requests.

"""

import os
from itertools import islice


class IteratorProxy(object):
    """docstring for IteratorProxy"""
    def __init__(self, i):
        self.i = i
        # self.i = chain.from_iterable(i)

    def __iter__(self):
        return self.i

    def __len__(self):
        if hasattr(self.i, '__len__'):
            return len(self.i)
        if hasattr(self.i, 'len'):
            return self.i.len
        if hasattr(self.i, 'fileno'):
            return os.fstat(self.i.fileno()).st_size

    def read(self, n):
        return "".join(islice(self.i, None, n))


class CaseInsensitiveDict(dict):
    """Case-insensitive Dictionary

    For example, ``headers['content-encoding']`` will return the
    value of a ``'Content-Encoding'`` response header."""

    @property
    def lower_keys(self):
        if not hasattr(self, '_lower_keys') or not self._lower_keys:
            self._lower_keys = dict((k.lower(), k) for k in list(self.keys()))
        return self._lower_keys

    def _clear_lower_keys(self):
        if hasattr(self, '_lower_keys'):
            self._lower_keys.clear()

    def __setitem__(self, key, value):
        lower_key = key.lower()
        existing_key = self.lower_keys.get(lower_key)
        if existing_key is not None:
            dict.__delitem__(self, existing_key)
        dict.__setitem__(self, lower_key, value)
        self._clear_lower_keys()

    def __delitem__(self, key):
        dict.__delitem__(self, key.lower())
        self._clear_lower_keys()

    def __contains__(self, key):
        return key.lower() in self.lower_keys()

    def __getitem__(self, key):
        return dict.__getitem__(self, key.lower())

    def get(self, key, default=None):
        return dict.get(self, key.lower(), default)


class LookupDict(dict):
    """Dictionary lookup object."""

    def __init__(self, name=None):
        self.name = name
        super(LookupDict, self).__init__()

    def __repr__(self):
        return '<lookup \'%s\'>' % (self.name)

    def __getitem__(self, key):
        # We allow fall-through here, so values default to None

        return self.__dict__.get(key, None)

    def get(self, key, default=None):
        return self.__dict__.get(key, default)
