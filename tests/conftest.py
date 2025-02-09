import pytest
from backend.business import VRResource, RawResource
from backend.persistence import (
    DataStorage,
)  # Assuming the class is in a module called datastorage
from icecream import ic
from .utils import get_blob


@pytest.fixture()
def data_storage():
    ds = DataStorage()
    yield ds
    DataStorage.wipe()


@pytest.fixture()
def raw_resource():
    yield {
        "name": "some",
        "pattern": RawResource("pattern", get_blob()),
        "media": RawResource("png", get_blob()),
    }
