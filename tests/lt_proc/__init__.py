#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import itertools
from subprocess import Popen, PIPE, call, STDOUT
from tempfile import mkdtemp
from shutil import rmtree

import signal
class Alarm(Exception):
    pass

class ltProcTest(unittest.TestCase):
    """Subclass and override inputs/expectedOutputs (and possibly other
stuff) to create new pretransfer tests."""

    inputs = [""]
    expectedOutputs = [""]
    expectedRetCodeFail = False

    def alarmHandler(self, signum, frame):
        raise Alarm

    def withTimeout(self, seconds, cmd, *args, **kwds):
        signal.signal(signal.SIGALRM, self.alarmHandler)
        signal.alarm(seconds)
        ret = cmd(*args, **kwds)
        signal.alarm(0)         # reset the alarm
        return ret



    def runTest(self):
        try:

            for inp, exp in zip(self.inputs, self.expectedOutputs):
                self.proc = Popen(['../lttoolbox/lt-proc', 'data/en-es.automorf.bin'], stdin = PIPE, stdout=PIPE, )
                self.assertEqual(self.proc.communicate(input=inp.encode('utf-8'))[0].strip().decode('utf-8')+"[][\n]", exp+"[][\n]")
                #strip and decode to remove '\n' at the end of output of communicate()
                #communicat() does the closing too.

            retCode = self.proc.poll()
            if self.expectedRetCodeFail:
                self.assertNotEqual(retCode, 0)
            else:
                self.assertEqual(retCode, 0)

        finally:
            pass

class SimpleInlineTagsTest(ltProcTest):
    inputs          = ["[{<b>}]two words[]",
                        "[<div>][<p>]white    [{<b>}]dog  [][][</p>][][</div>]"]

    expectedOutputs = [ "[{<b>}]^two/two<num><sp>$ [{<b>}]^words/word<n><pl>$[]",
                        "[<div>][<p>]^white/white<n><sg>/white<adj><sint>$    [{<b>}]^dog/dog<n><sg>$  [][][</p>][][</div>]"]


class TagTransferTest(ltProcTest):
    inputs          = ["a[{<b>}] y z[]",
                        "a[{<b>}]y z[]",
                        "a [{<b>}] y z[]",
                        "[{<b>}]two[] other [{<i>}]words[]"]

    expectedOutputs = ["^a/a<det><ind><sg>$ [{<b>}]^y/*y$ [{<b>}]^z/*z$[]",
                        "^a/a<det><ind><sg>$[{<b>}]^y/*y$ [{<b>}]^z/*z$[]",
                        "^a/a<det><ind><sg>$ [{<b>}]^y/*y$  [{<b>}]^z/*z$[]",
                        "[{<b>}]^two/two<num><sp>$[] ^other/other<det><ind><sp>$ [{<i>}]^words/word<n><pl>$[]"]

