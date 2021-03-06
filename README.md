# MultiHash [![v2.0.1](https://img.shields.io/badge/version-2.0.1-blue.svg)](https://github.com/bnbalsamo/MultiHash/releases)

[![CI](https://github.com/bnbalsamo/MultiHash/workflows/CI/badge.svg?branch=master)](https://github.com/bnbalsamo/MultiHash/actions)
[![Coverage](https://codecov.io/gh/bnbalsamo/MultiHash/branch/master/graph/badge.svg)](https://codecov.io/gh/bnbalsamo/MultiHash/)
 [![Documentation Status](https://readthedocs.org/projects/bnb-MultiHash/badge/?version=latest)](http://bnb-MultiHash.readthedocs.io/en/latest/?badge=latest)
[![Updates](https://pyup.io/repos/github/bnbalsamo/MultiHash/shield.svg)](https://pyup.io/repos/github/bnbalsamo/MultiHash/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Wraps hashlib.hash instances for easily computing multiple hashes at the same time.

See the full documentation at https://bnb-MultiHash.readthedocs.io

A convenience class for computing multiple hashes at the same time from a single source.

This class optimizes disk reads per computation, but does not implement threading or multiprocessing.

Provides the [same interface as hashlib.hash classes](https://docs.python.org/3/library/hashlib.html#hashlib.hash.digest_size) with properties returning dictionaries of results using the hash's name as the key, excluding .name, which returns a MultiHash specific name.

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
>>> from io import BytesIO
>>> MultiHash.from_Stream(BytesIO(urandom(256)), hashers=['md5', 'sha256']).hexdigest()
{'md5': 'bd5c3a82f88ed4d903f4c30a21b827b6', 'sha256': 'a799b79935c54af47704d3b8421c83989b0cbc4078dd5a94aa8036a4912ae27e'}
```

# Installation
- ```$ git clone https://github.com/bnbalsamo/MultiHash.git```
- ```$ cd MultiHash```
    - If you would like to install the pinned dependencies, run ```pip install -r requirements.txt```
- ```$ python -m pip install .```

# Development

## Quickstart

To quickly install + configure a development environment...

Install [pyenv](https://github.com/pyenv/pyenv), [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv),
and [xxenv-latest](https://github.com/momo-lab/xxenv-latest) and copy the following into your terminal while
in the repository root.

```bash
[[ `type -t pyenv` ]] && \
[ -s "$PYENV_ROOT/plugins/pyenv-virtualenv" ] && \
[ -s "$PYENV_ROOT/plugins/xxenv-latest" ] && \
pyenv latest install -s 3.8 && \
PYENV_LATEST_38=$(pyenv latest -p 3.8) && \
pyenv latest install -s 3.7 && \
PYENV_LATEST_37=$(pyenv latest -p 3.7) && \
pyenv latest install -s 3.6 && \
PYENV_LATEST_36=$(pyenv latest -p 3.6) && \
pyenv virtualenv "$PYENV_LATEST_38" "MultiHash" && \
pyenv local "MultiHash" "$PYENV_LATEST_38" "$PYENV_LATEST_37" "$PYENV_LATEST_36" && \
pip install -e .[dev,tests,docs]
```

## Manual Configuration

If you choose not to use the quickstart script you will need to...

- Create a virtual environment
- Install the development dependencies
    - `pip install -e .[dev,tests,docs]`
- Configure tox so that it can access all relevant python interpreters

## Running Tests
```
$ inv run.tests
```

## Running autoformatters
```
$ inv run.autoformatters
```

## Pinning Dependencies
```
$ inv pindeps
```

# Author
Brian Balsamo <Brian@BrianBalsamo.com>

_Created using [bnbalsamo/cookiecutter-pypackage](https://github.com/bnbalsamo/cookiecutter-pypackage) v0.38.0_
