"""Tests for MultiHash."""
from io import BytesIO
from os import urandom
from tempfile import NamedTemporaryFile

import pytest

import multihash
from multihash import MultiHash


def test_version_available():
    """Test the version dunder is available on the module."""
    assert getattr(multihash, "__version__", None) is not None


def test_from_precomputed():
    """Test that the hashing operation is accurate."""
    assert MultiHash(b"This is a test", hashers=["md5", "sha256"]).hexdigest() == {
        "sha256": "c7be1ed902fb8dd4d48997c6452f5d7e509fbcdbe2808b16bcf4edce4c07d14e",
        "md5": "ce114e4501d2f4e2dcea3e17b546f339",
    }


def test_update():
    """Test the upate functionality, using precomputed hashes."""
    hasher = MultiHash(hashers=["md5", "sha256"])
    hasher.update(b"this is some data")
    hasher.update(b"and this is some more")
    assert hasher.hexdigest() == {
        "md5": "8dcdbfc187e97b7f8817b7fe857c7635",
        "sha256": "a88897eb17993ace17bdb55f60bce7afc37156a939c3b217d4cb31fd2ade5848",
    }


def test_file_hash():
    """Test hashing a file, using precomputed hashes."""
    precomputed_hashes = {
        "md5": "4ca3f52a8a3c1643708cce5e9a919b43",
        "sha256": "a2c56fb21bee151494b5d3bb40ed3e3d357b2014c82bb937f0d181dd43124fea",
    }
    with NamedTemporaryFile() as test_file:
        with open(test_file.name, "wb") as file_object:
            file_object.write(b"blahblahblahblahblahblahblah")
        assert (
            MultiHash.from_filepath(
                test_file.name, hashers=["md5", "sha256"]
            ).hexdigest()
            == precomputed_hashes
        )


def test_data_in_init():
    """Test hashing data supplied in the init."""
    precomputed_hashes = {
        "md5": "4ca3f52a8a3c1643708cce5e9a919b43",
        "sha256": "a2c56fb21bee151494b5d3bb40ed3e3d357b2014c82bb937f0d181dd43124fea",
    }
    assert (
        MultiHash(
            data=b"blahblahblahblahblahblahblah", hashers=["md5", "sha256"]
        ).hexdigest()
        == precomputed_hashes
    )


def test_stream():
    """Test hashing directly from a stream works."""
    result = MultiHash.from_stream(
        BytesIO(urandom(1024 * 50)), hashers=["md5", "sha256"]
    ).hexdigest()
    assert "md5" in result
    assert "sha256" in result


def test_hasher_info():
    """Exercise the standard harsher interface."""
    mh = MultiHash.from_stream(BytesIO(urandom(1024)), hashers=["md5", "sha256"])
    digest_sizes = mh.digest_size
    assert isinstance(digest_sizes, dict)
    assert digest_sizes == {"sha256": 32, "md5": 16}
    block_sizes = mh.block_size
    assert isinstance(digest_sizes, dict)
    assert block_sizes == {"sha256": 64, "md5": 64}
    assert mh.name.startswith("MultiHash[")
    assert "md5" in mh.name
    assert "sha256" in mh.name
    digests = mh.digest()
    assert "md5" in digests
    assert "sha256" in digests
    for value in digests.values():
        assert isinstance(value, bytes)
    hex_digests = mh.hexdigest()
    assert "md5" in hex_digests
    assert "sha256" in hex_digests
    for value in hex_digests:
        assert isinstance(value, str)


if __name__ == "__main__":
    pytest.main()
