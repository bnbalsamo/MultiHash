# MultiHash

v1.1.0

[![Build Status](https://travis-ci.org/bnbalsamo/MultiHash.svg?branch=master)](https://travis-ci.org/bnbalsamo/MultiHash) [![Coverage Status](https://coveralls.io/repos/github/bnbalsamo/MultiHash/badge.svg?branch=master)](https://coveralls.io/github/bnbalsamo/MultiHash?branch=master)

A convenience class for computing multiple hashes at the same time from a single source.

This class optimizes disk reads per computation, but does not implement threading or multiprocessing.

Provides the [same interface as hashlib.hash classes](https://docs.python.org/3/library/hashlib.html#hashlib.hash.digest_size) with properties returning dictionaries of results using the hash's name as the key, excluding .name, which returns a MultiHash specific name, usable with ```multihash.new()```. 

The class provides an ```additional_hashers``` set where other classes conforming the hashlib.hash interface, or classes which override existing hashlib.hash classes functionalities may be placed in order for instances of MultiHash to utilize them.

# Usage

Computing the hash(es) of some data in RAM
```
>>> from multihash import MultiHash
>>> MultiHash(b"This is a test", hashers=['md5', 'sha256']).hexdigest()
{'sha256': 'c7be1ed902fb8dd4d48997c6452f5d7e509fbcdbe2808b16bcf4edce4c07d14e', 'md5': 'ce114e4501d2f4e2dcea3e17b546f339'}
```

Utilizing the ```.update()``` method
```
>>> from multihash import MultiHash
>>> x = MultiHash(hashers=['md5', 'sha256'])
>>> x.update(b"this is some data")
>>> x.update(b"and this is some more")
>>> x.hexdigest()
{'md5': '8dcdbfc187e97b7f8817b7fe857c7635', 'sha256': 'a88897eb17993ace17bdb55f60bce7afc37156a939c3b217d4cb31fd2ade5848'}
```

Computing the hash(es) of a file
```
>>> from multihash import MultiHash
>>> with open('test_file', 'wb') as f:
...     f.write(b"blahblahblahblahblahblahblah")
>>> MultiHash.from_filepath('test_file', hashers=['md5', 'sha256']).hexdigest()
{'md5': '4ca3f52a8a3c1643708cce5e9a919b43', 'sha256': 'a2c56fb21bee151494b5d3bb40ed3e3d357b2014c82bb937f0d181dd43124fea'}
```

Computing the hash(es) of a stream/file like object/thing that implements ```.read()```
```
>>> from os import urandom
>>> class PretendStream:
...     def __init__(self, streamlen):
...             self.streamlen = streamlen
...     def read(self, x):
...             if self.streamlen < 1:
...                     return False
...             self.streamlen = self.streamlen - x
...             return urandom(x)
... 
>>> x = PretendStream(1024*50)
>>> MultiHash.from_flo(x, hashers=['md5', 'sha256']).hexdigest()
{'md5': 'bd5c3a82f88ed4d903f4c30a21b827b6', 'sha256': 'a799b79935c54af47704d3b8421c83989b0cbc4078dd5a94aa8036a4912ae27e'}
```

# Author
Brian Balsamo <brian@brianbalsamo.com>
