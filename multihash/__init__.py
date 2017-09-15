"""
multihash
"""

from hashlib import new as _new
from json import loads, dumps

__author__ = "Brian Balsamo"
__email__ = "brian@brianbalsamo.com"
__version__ = "1.0.2"


additional_hashers = set()


def new(hashname):
    """
    Wraps hashlib.new
    Supports MultiHash instances and
        adding additional hash classes

    Input - A hash name as a str
    Output - A hashing object
    """
    if hashname.startswith("MultiHash"):
        hashers = loads(hashname[9:])
        return MultiHash(hashers=hashers)
    try:
        for x in additional_hashers:
            if x.name == hashname:
                return x()
        raise ValueError("unsupported hash type {}".format(hashname))
    except ValueError:
        return _new(hashname)


class MultiHash:
    """
    A class which uses effecient disk reads to compute multiple hashes
    """

    def __init__(self, data=None, hashers=[]):
        """
        Create a new MultiHash instance

        __Args__

        * data: some binary data to seed all the hashers with
        * hashers: Instances of classes conforming to the
            hashlib.hash interface
        """
        self._hashers = set()
        self._chunksize = None
        self.set_hashers(hashers)
        if data:
            self.update(data)

    @classmethod
    def from_filepath(cls, fp, hashers=[], chunksize=2**8):
        """
        Instantiate a new MultiHash, hash a file
            located at some file path

        __Args__

        1. fp (str): A file path

        __KWArgs__

        * hashers: Instances of classes conforming to the
            hashlib.hash interface
        * chunksize (int): How many bytes to read into RAM
            in one go
        """
        with open(fp, 'rb') as f:
            return cls.from_flo(f, hashers=hashers, chunksize=chunksize)

    @classmethod
    def from_flo(cls, flo, hashers=[], chunksize=2**8):
        """
        Instantiate a new MultiHash, hash a .read()-able thing

        __Args__

        1. flo: An object which implements .read()

        __KWArgs__

        * hashers: Instances of classes conforming to the
            hashlib.hash interface
        * chunksize (int): How many bytes to read into RAM
            in one go
        """
        x = cls(hashers=hashers)
        chunk = flo.read(chunksize)
        while chunk:
            x.update(chunk)
            chunk = flo.read(chunksize)
        return x

    def get_hashers(self):
        return self._hashers

    def set_hashers(self, hashers):
        for x in hashers:
            if isinstance(x, str):
                self._hashers.add(new(x))
            else:
                self._hashers.add(x)

    def del_hashers(self):
        self._hashers = set()

    def get_name(self):
        """
        Returns a name for the MultiHash instance
        multihash.new() supports reading these names
        """
        return "MultiHash{}".format(
            str(
                dumps([x.name for x in self.hashers])
            )
        )

    # For the rest of these see the hashlib.hash interface
    # https://docs.python.org/3/library/hashlib.html#hashlib.hash.digest_size
    # All returned values are dictionaries where the keys are the
    # name attribute and the values are the restult of calling the
    # corresponding function on the embedded instance

    def get_digest_size(self):
        return {x.name: x.digest_size for x in self.hashers}

    def get_block_size(self):
        return {x.name: x.block_size for x in self.hashers}

    def update(self, data):
        for x in self.hashers:
            x.update(data)

    def digest(self):
        return {x.name: x.digest() for x in self.hashers}

    def hexdigest(self):
        return {x.name: x.hexdigest() for x in self.hashers}

    def copy(self):
        return {x.name: x.copy() for x in self.hashers}

    hashers = property(get_hashers, set_hashers, del_hashers)
    digest_size = property(get_digest_size)
    block_size = property(get_block_size)
    name = property(get_name)
