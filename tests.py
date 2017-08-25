import unittest
from multihash import MultiHash, new
from tempfile import NamedTemporaryFile
from os import urandom


class ReadMeTests(unittest.TestCase):
    def testRAM(self):
        self.assertEqual(
            MultiHash(b"This is a test", hashers=['md5', 'sha256']).hexdigest(),
            {
                'sha256': 'c7be1ed902fb8dd4d48997c6452f5d7e509fbcdbe2808b16bcf4edce4c07d14e',
                'md5': 'ce114e4501d2f4e2dcea3e17b546f339'
            }
        )

    def testUpdate(self):
        x = MultiHash(hashers=['md5', 'sha256'])
        x.update(b"this is some data")
        x.update(b"and this is some more")
        self.assertEqual(
            x.hexdigest(),
            {'md5': '8dcdbfc187e97b7f8817b7fe857c7635',
             'sha256': 'a88897eb17993ace17bdb55f60bce7afc37156a939c3b217d4cb31fd2ade5848'}
        )

    def testFile(self):
        test_file = NamedTemporaryFile()
        with open(test_file.name, 'wb') as f:
            f.write(b"blahblahblahblahblahblahblah")
        self.assertEqual(
            MultiHash.from_filepath(test_file.name, hashers=['md5', 'sha256']).hexdigest(),
            {
                'md5': '4ca3f52a8a3c1643708cce5e9a919b43',
                'sha256': 'a2c56fb21bee151494b5d3bb40ed3e3d357b2014c82bb937f0d181dd43124fea'
            }
        )
        del test_file

    def testFlo(self):
        class PretendStream:
            def __init__(self, streamlen):
                    self.streamlen = streamlen

            def read(self, x):
                    if self.streamlen < 1:
                            return False
                    self.streamlen = self.streamlen - x
                    return urandom(x)

        x = PretendStream(1024*50)
        r = MultiHash.from_flo(x, hashers=['md5', 'sha256']).hexdigest()
        self.assertTrue("md5" in r)
        self.assertTrue("sha256" in r)

    def testNew(self):
        x = MultiHash(hashers=['md5', 'sha256'])
        y = new(x.name)
        self.assertEqual(set(n.name for n in x.hashers),
                         set(m.name for m in y.hashers))


if __name__ == '__main__':
    unittest.main()
