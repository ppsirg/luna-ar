import os
import pytest
from backend.business import VRResource


def test_create(raw_resource):
    created = VRResource.create(**raw_resource)

    assert type(created) is VRResource
    assert created.name == raw_resource["name"], "not correct name"
    assert os.path.exists(created.media), "not media"
    assert os.path.exists(created.pattern), "not pattern"


def test_remove(raw_resource, data_storage):
    created = VRResource.create(**raw_resource)
    result = VRResource.remove(created._id)

    assert not data_storage.get(created._id), "not deleted"
    assert result is True
