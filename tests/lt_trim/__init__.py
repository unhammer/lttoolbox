# -*- coding: utf-8 -*-

import unittest

from subprocess import call
from tempfile import mkdtemp
from shutil import rmtree

class Trim(unittest.TestCase):
    def runTest(self):
        tmpd = mkdtemp()
        try:
            self.assertEqual(0, call(["../lttoolbox/lt-comp",
                                      "lr",
                                      "data/minimal-mono.dix",
                                      tmpd+"/minimal-mono.bin"]))
            self.assertEqual(0, call(["../lttoolbox/lt-comp",
                                      "lr",
                                      "data/minimal-bi.dix",
                                      tmpd+"/minimal-bi.bin"]))
            self.assertEqual(0, call(["../lttoolbox/lt-trim",
                                      tmpd+"/minimal-mono.bin",
                                      tmpd+"/minimal-bi.bin",
                                      tmpd+"/minimal-trimmed.bin"]))
        finally:
            rmtree(tmpd)
