import yaml
import os
import json


class FileStore(object):

    def __init__(self, filename):
        self.filename = filename
        self.data = self.load()

    def load(self) -> dict:
        return self._load()

    def dump(self) -> None:
        if self.data == self.load():
            self._dump()

    def _load(self) -> dict:
        """
        store specific loading of data needs to override this function

        :return: configurations as a dict
        """
        pass

    def _dump(self) -> None:
        """
        store specific saving of data needs to override this function
        """

    def update(self, new_data: dict = None, **kwargs) -> None:
        self.data.update(new_data, **kwargs)

    def add_config(self, key, value):
        if self.data.get(key):
            raise KeyError(f"config {key} already exists")
        else:
            self.data[key] = value

    def remove_config(self, key):
        del self.data[key]

    def __repr__(self) -> str:
        return f"FileStore({self.load()})"


class YAMLFileStore(FileStore):

    def _load(self) -> dict:
        if os.path.isfile(self.filename):
            with open(self.filename, 'r') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
            if data:
                return data
        return {}

    def _dump(self) -> None:
        with open(self.filename, 'w') as f:
            yaml.safe_dump(self.data, f)

    def __repr__(self) -> str:
        return f"YAMLFileStore({self.load()})"


class JSONFileStore(FileStore):

    def _load(self) -> dict:
        if os.path.isfile(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                if data:
                    return data
        return {}

    def _dump(self) -> None:
        with open(self.filename, 'w') as f:
            json.dump(self.data, f)

    def __repr__(self) -> str:
        return f"YAMLFileStore({self.load()})"


class FileStoreException(Exception):
    pass


class FileStoreNotFound(FileStoreException):
    pass


class FileStoreDetectionFailedException(FileStoreException):
    pass


def get_store(filename: str, store_type: str = "auto") -> FileStore:
    FILESTORE_EXTENSION = {
        "yaml": ["yaml", "yml"],
        "json": ["json"]
    }

    # if store_type is auto, the store type is guessed from file extension
    if store_type == "auto":
        file_ext = filename.split(".")[-1]
    else:
        file_ext = ""

    if store_type.lower() in FILESTORE_EXTENSION["yaml"] \
            or file_ext.lower() in FILESTORE_EXTENSION["yaml"]:
        return YAMLFileStore(filename)
    elif store_type.lower() in FILESTORE_EXTENSION["json"] \
            or file_ext.lower() in FILESTORE_EXTENSION["json"]:
        return JSONFileStore(filename)
    else:
        raise FileStoreDetectionFailedException(f"Failed to identify type of FileStore {filename}")
