import os
import uuid
from .persistence import DataStorage
from .constants import CONTENT_TYPE_SUFFIX
from typing import NamedTuple
from settings import MEDIA_FOLDER, PATTERN_FOLDER


class RawResource(NamedTuple):
    type: str
    content: bytes

    def save(self, folder: str, name_base: str):
        path = os.path.join(folder, f"{name_base}.{self.suffix}")
        try:
            with open(path, "+bw") as fl:
                fl.write(self.content)
            return path
        except Exception as err:
            print(
                f"error on content save: {err}, args: {folder}, {name_base}, {self.suffix}"
            )
            return False

    @property
    def suffix(self):
        return CONTENT_TYPE_SUFFIX.get(self.type, "txt")


class VRResource:
    db = DataStorage()

    def __init__(
        self, _id: str, name: str = None, pattern: str = None, media: str = None
    ):
        self._id = _id
        if any((a is None for a in (name, media, pattern))):
            info = self.db.get(_id)
            if info:
                for k in ("pattern", "media", "name"):
                    setattr(self, k, info[k])
        else:
            self.name = name
            self.pattern = pattern
            self.media = media

    @property
    def dict(self):
        return {a: getattr(self, a) for a in ("pattern", "media", "name", "_id")}

    @property
    def public_info(self):
        return {a: getattr(self, a) for a in ("name", "_id")}
    
    @property
    def public_media(self):
        return os.path.basename(self.media)

    @property
    def public_pattern(self):
        return os.path.basename(self.pattern)

    @classmethod
    def list(cls):
        return cls.db.list()

    @classmethod
    def create(cls, name: str, pattern: RawResource, media: RawResource):
        # Create unique IDs for the files using uuid4
        res_id = str(uuid.uuid4())

        # Save bytes objects to resources folder (pseudo-code, not actual file saving logic)
        pattern_path = pattern.save(PATTERN_FOLDER, res_id)
        media_path = media.save(MEDIA_FOLDER, res_id)

        # Create an instance of DataStorage and add the resource
        data_storage = DataStorage()
        data_storage.add(
            res_id, {"name": name, "media": media_path, "pattern": pattern_path}
        )

        # Return an instance of VRResource with the created resource details
        return cls(res_id, name=name, pattern=pattern_path, media=media_path)

    @classmethod
    def remove(cls, id: str):
        data_storage = DataStorage()
        result = data_storage.delete(id)
        return result
