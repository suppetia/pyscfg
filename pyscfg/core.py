from typing import Union

from pyscfg.stores import FileStore, get_store


class Configs:

    def __init__(self, store: FileStore = None):
        self.store = store

    def _load(self):
        return self.store.load()

    def _save(self):
        return self.store.dump()

    def _update(self, data=None, save=True, **kwargs):
        self.store.update(data, **kwargs)
        if save:
            self._save()

    def _remove(self, key, save=True):
        self.store.remove_config(key)
        if save:
            self._save()

    def init_if_not_exists(self, key, default, save=True):
        """
        assign value default to configuration key if no value is stored for key

        :param key: the configuration name
        :param default: configurations default value
        :param save: whether the update should be saved in store
        """
        data = self._load()
        if key in data:
            return
        self._update({key: default}, save=save)

    def __getitem__(self, item):
        data = self._load()
        return data[item]

    def __setitem__(self, key, value):
        self._update({key: value})

    def __delitem__(self, key):
        self._remove(key)


class SimpleConfigs(Configs):

    def __init__(self, file: str = "configs.yml", store_type: str = "auto", defaults: Union[dict, str] = None):

        self.store = get_store(filename=file, store_type=store_type)

        # init the configs with some default values if there are no values stored for this values
        if defaults:
            if isinstance(defaults, str):
                defaults = get_store(filename=defaults).load()
            for key, value in defaults.items():
                self.init_if_not_exists(key=key, default=value, save=False)
            self._save()

