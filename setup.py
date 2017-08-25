from setuptools import setup, find_packages

def readme():
    with open("README.md", 'r') as f:
        return f.read()

setup(
    name = "multihash",
    description = "wraps hashlib.hash instances for easily computing " + \
        "multiple hashes at the same time",
    version = "1.0.0",
    long_description = readme(),
    author = "Brian Balsamo",
    author_email = "brian@brianbalsamo.com",
    packages = find_packages(
        exclude = [
        ]
    )
)
