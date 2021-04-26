"""
MultiHash.

Wraps hashlib.hash instances for easily computing multiple hashes at the same time.
"""

__author__ = "Brian Balsamo"
__email__ = "Brian@BrianBalsamo.com"
__version__ = "2.0.0"

import hashlib
from json import dumps
from os import PathLike
from typing import Any, BinaryIO, Dict, Iterable, Optional, Set, Union

# There's some weirdness here wrt typing checking the Protocol import itself.
# See https://github.com/python/mypy/issues/4427
try:
    from typing import Protocol  # type: ignore
except ImportError:  # Support python<3.8
    from typing_extensions import Protocol  # type: ignore


# Protocols for type checking


class HasherType(Protocol):  # pragma: no cover
    """
    Protocol for "hashers".

    These are classes that actually compute the hashes.
    """

    name: str
    digest_size: int
    block_size: int

    def update(self, data: bytes) -> None:
        """Update the hasher."""
        ...

    def digest(self) -> bytes:
        """Produce a digest."""
        ...

    def hexdigest(self) -> str:
        """Produce a hexdigest."""
        ...

    def copy(self) -> "HasherType":
        """Produce a copy of the hasher."""
        ...


class HasherFactory(Protocol):  # pragma: no cover  # pylint: disable=R0903
    """
    Protocol for "hasher factories".

    These are objects/functions that return instances that implement `HasherType`
    when called, eg: `hashlib.md5`.
    """

    def __call__(self, data: bytes = b"") -> HasherType:
        """Return a hasher."""
        ...


class MultiHash:
    """A class which effeciently generates multiple hashes."""

    def __init__(
        self,
        data: Optional[bytes] = None,
        hashers: Optional[Iterable[Union[HasherType, str]]] = None,
    ):
        """
        Create a new MultiHash instance.

        :param data: Binary data to seed all the hashers with
        :param hashers: Instances of classes conforming to the
            hashlib.hash interface, or names of hashes appropriate for `new()`
        """
        self._hashers: Set[HasherType] = set()
        if hashers is not None:
            self._set_hashers(hashers)
        if data:
            self.update(data)

    @classmethod
    def from_filepath(
        cls,
        filepath: PathLike,
        hashers: Iterable[Union[HasherType, str]] = None,
        chunksize: int = 128000000,  # 128MB
    ) -> "MultiHash":
        """
        Instantiate a new MultiHash and hash a file located at some file path.

        :param filepath: A file path
        :param hashers: Instances of classes conforming to the
            hashlib.hash interface, or names of hashes appropriate for `new()`
        :param chunksize: How many bytes to read into RAM at once
        """
        with open(filepath, "rb") as stream:
            return cls.from_stream(stream, hashers=hashers, chunksize=chunksize)

    @classmethod
    def from_stream(
        cls,
        stream: BinaryIO,
        hashers: Iterable[Union[HasherType, str]] = None,
        chunksize: int = 128000000,  # 128MB
    ) -> "MultiHash":
        """
        Instantiate a new MultiHash and hash a .read()-able thing.

        :param stream: An object which implements .read()
        :param hashers: Instances of classes conforming to the
            hashlib.hash interface
        :param chunksize: How many bytes to read into RAM at once
        """
        multihash = cls(hashers=hashers)
        chunk = stream.read(chunksize)
        while chunk:
            multihash.update(chunk)
            chunk = stream.read(chunksize)
        return multihash

    def _get_hashers(self) -> Set[HasherType]:
        """Return a set of all the contained "hashers"."""
        return self._hashers

    def _set_hashers(self, hashers: Iterable[Union[HasherType, str]]) -> None:
        """
        Set the _hashers attribute.

        Handles iterables of "hashers" or name strings.
        """
        for hasher in hashers:
            if isinstance(hasher, str):
                self._hashers.add(hashlib.new(hasher))
            else:
                self._hashers.add(hasher)

    def _del_hashers(self) -> None:
        """Delete the _hashers attribute data."""
        self._hashers = set()

    def _get_name(self) -> str:
        """Return a name for the MultiHash instance."""
        return "MultiHash{}".format(str(dumps([x.name for x in self.hashers])))

    def __repr__(self) -> str:
        """Display a nice name if printed."""
        return self._get_name()

    def update(self, data: bytes) -> None:
        """
        Update all the underlying hashes with the supplied data.

        :param data: The data to update the hashes with.
        """
        for hasher in self.hashers:
            hasher.update(data)

    def _call_all_hashers(self, method_name: str, *args, **kwargs) -> Dict[str, Any]:
        """
        Call a method on all the hashers.

        Returns a dict, hasher names as keys, return values as values
        """
        return {
            hasher.name: getattr(hasher, method_name)(*args, **kwargs)
            for hasher in self.hashers
        }

    def _get_attr_from_all_hashers(self, attr_name: str) -> Dict[str, Any]:
        """
        Get an attr from all the hashers.

        Returns a dict, hasher names as keys, attr values as values
        """
        return {hasher.name: getattr(hasher, attr_name) for hasher in self.hashers}

    # For the rest of these see the hashlib.hash interface
    # https://docs.python.org/3/library/hashlib.html#hashlib.hash.digest_size
    # All returned values are dictionaries where the keys are the
    # name attribute and the values are the restult of calling the
    # corresponding function on the embedded instance

    def _get_digest_size(self) -> Dict[str, int]:
        """Return a dict of all the underlying digest sizes."""
        return self._get_attr_from_all_hashers("digest_size")

    def _get_block_size(self) -> Dict[str, int]:
        """Return a dict of all the underlying block sizes."""
        return self._get_attr_from_all_hashers("block_size")

    def digest(self, *args, **kwargs) -> Dict[str, bytes]:
        """Return a dictionary containing all the digests."""
        return self._call_all_hashers("digest", *args, **kwargs)

    def hexdigest(self, *args, **kwargs) -> Dict[str, str]:
        """Return a dictionary containing all the hexdigests."""
        return self._call_all_hashers("hexdigest", *args, **kwargs)

    def copy(self, *args, **kwargs) -> Dict[str, HasherType]:
        """Return a dictionary containing copies of all the hashers."""
        return self._call_all_hashers("copy", *args, **kwargs)

    hashers = property(_get_hashers, _set_hashers, _del_hashers)
    digest_size = property(_get_digest_size)
    block_size = property(_get_block_size)
    name = property(_get_name)
