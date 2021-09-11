from typing import Dict, Union, Any
from stores import DataStore, RamStore

import logging
log = logging.getLogger(__file__)


class ConfigsDict:

    def __init__(self,
                 data: Dict[str, Any] = None,
                 super_dict: "ConfigsDict" = None,
                 prefix: str = "",
                 data_store: DataStore = None):
        # if not isinstance(data, (dict, ConfigsDict)):
        #     raise TypeError(f"data should be dict or ConfigsDict but is {type(data)}")
        # self._configs: Dict[str, Any] = self._flatten_dict(data)
        self._super_dict = super_dict
        self._prefix = prefix if not prefix.startswith(".") else prefix[1:]
        if prefix == "":
            self._data_store = data_store if data_store is not None else RamStore()
        else:
            self._data_store = None

        if self._data_store is not None:
            if data is not None:
                if not self._data_store.is_empty() \
                        and not self._flatten_dict(data) == self._flatten_dict(self._data_store.load()):
                    raise ValueError(f":param data: and :param data_store: are specified but the data in the DataStore does not equal the data passed to the constructor.")
                else:
                    self._configs = self._flatten_dict(data)
                    self.save()
            else:
                self._configs = self._flatten_dict(self._data_store.load())
        else:
            self._configs = self._flatten_dict(data) if data is not None else dict()

    def _flatten_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Flatten a dict as subdict keys are merged into the dict using a '.' to separate different levels.
        :param data: the fict to flatten
        :return:
        """
        subdicts = [k for k, v in data.items() if isinstance(v, (dict, ConfigsDict))]

        for k in data.keys():
            if not self._is_valid_key(k):
                raise ValueError(f"invalid key: '{k}'")

        flattened_dict = {f"{k}.{sub_k}": sub_v for k in subdicts
                          for sub_k, sub_v in self._flatten_dict(data[k]).items()}
        flattened_dict.update({k: v for k,v in data.items() if not isinstance(v, (dict, ConfigsDict))})

        return flattened_dict

    @property
    def configs(self):
        return self._configs

    @configs.setter
    def configs(self, value):
        self._configs = self._flatten_dict(value)

    def _filter_dict(self, d:Dict[str, Any], prefix: str) -> Dict[str, Any]:
        return {k[len(prefix)+1:]: v for k,v in d.items() if k.startswith(f"{prefix}.")}

    def _get_subdict(self, key: str):
        levels = key.split(".")
        if len(levels) == 1:
            return ConfigsDict(self._filter_dict(self._configs, key),
                               super_dict=self,
                               prefix=".".join([self._prefix, key]))
        else:
            return ConfigsDict(self._filter_dict(self._configs, levels[0]),
                               super_dict=self,
                               prefix=".".join([self._prefix, levels[0]]))._get_subdict(".".join(levels[1:]))

    def save(self):
        if self._data_store is not None:
            self._data_store.save(self.as_dict())

    def _is_valid_key(self, key):
        """
        Check if :param:key is valid (is string).
        :return:
        """
        if not isinstance(key, str):
            return False
        # if "." in key:
        #     return False
        return True

    def is_empty(self) -> bool:
        return self._configs == {}

    def as_dict(self) -> dict:
        dict_repr = {}
        for k, v in self._configs.items():
            levels = k.split(".")
            dict_repr[levels[0]] = self._get_subdict(levels[0]).as_dict() if len(levels) > 1 else v

        return dict_repr

    def _get(self, key, as_dict: bool = False) -> Union["ConfigsDict", Any]:
        levels = key.split(".")
        if len(levels) == 1:
            if key in self._configs.keys():
                return self._configs[key]
            else:
                subdict = self._get_subdict(key)
                if not subdict.is_empty():
                    return subdict.as_dict() if as_dict else subdict
                else:
                    raise KeyError(key)
        else:
            return self._get_subdict(levels[0])._get(".".join(levels[1:]), as_dict=as_dict)

    def get(self, key, default=None, as_dict: bool = True) -> Union["ConfigsDict", Any]:
        try:
            return self._get(key, as_dict=as_dict)
        except KeyError:
            return default

    def __getitem__(self, key):
        return self.get(key, as_dict=False)

    def __getattr__(self, item):
        return self.get(item, as_dict=False)

    def _set(self, key, value):
        if not self._is_valid_key(key):
            raise ValueError(f"invalid key: {key}")
        self._configs.update(self._flatten_dict({key: value}))

        d = self
        while d._super_dict is not None:
            d_ = d._super_dict

            new_dict = d_.as_dict()
            new_dict.update({d._prefix.split(".")[-1]: d._configs})
            d_._configs = self._flatten_dict(new_dict)
            d = d_
            print(d)

        # save changes
        d.save()

    def __setitem__(self, key, value):
        self._set(key, value)
    #
    # def __setattr__(self, key, value):
    #     self._set(key, value)

    def __repr__(self):
        return self._configs

    def __str__(self):
        return f"ConfigsDict({str(self._configs)})"



if __name__ == "__main__":
    from pprint import pprint
    import sys
    from stores import get_store

    d = {
        "a": {
            "a": {
                "a": {
                    "a": {
                        "a": 1,
                        "b": 2
                    }
                }
            },
            "b": 10
        },
        "b": 2,
        #"a.2": 3
    }

    cfg_dict = ConfigsDict(data_store=get_store("configs.yaml"))
    print(cfg_dict._configs)
    print(cfg_dict._data_store)

    cfg_dict["a"]["c"] = dict(a="B", b="B")
    print(cfg_dict._configs)
    # print(cfg_dict["a"]["c"]._prefix)
    # cfg_dict["a"]["c"]["a"] = "B"
    print(cfg_dict._configs)

    # print(cfg_dict.get("a.a"))
    # print(cfg_dict.get("a"))
    # print(cfg_dict["a"])
    # print(cfg_dict["a"]["a"])
    # print(cfg_dict.a.a)

    # sub1 = cfg_dict._get_subdict("a.a")
    # print(sub1._configs)
    # print(sub1._super_dict)

    # print(cfg_dict._get_subdict("a.a.a.a")._configs)
    # print(cfg_dict._get_subdict("a.a.a.a")._super_dict)

    # pprint(cfg_dict.as_dict())
    # print(cfg_dict["a.a.a.a.a"])

    # print(cfg_dict["a.a.a.a.a"])
    # print(cfg_dict["a.a.a.a"])

