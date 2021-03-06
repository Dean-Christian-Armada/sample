#!/usr/bin/env python
"""Tests for stream_slice."""

import string
import StringIO

import unittest2

from apitools.base.py import buffered_stream
from apitools.base.py import exceptions


class BufferedStreamTest(unittest2.TestCase):

  def setUp(self):
    self.stream = StringIO.StringIO(string.letters)
    self.value = self.stream.getvalue()
    self.stream.seek(0)

  def testEmptyBuffer(self):
    bs = buffered_stream.BufferedStream(self.stream, 0, 0)
    self.assertEqual('', bs.read(0))
    self.assertEqual(0, bs.stream_end_position)

  def testOffsetStream(self):
    bs = buffered_stream.BufferedStream(self.stream, 50, 100)
    self.assertEqual(len(self.value), len(bs))
    self.assertEqual(self.value, bs.read(len(self.value)))
    self.assertEqual(50 + len(self.value), bs.stream_end_position)

  def testUnexhaustedStream(self):
    bs = buffered_stream.BufferedStream(self.stream, 0, 50)
    self.assertEqual(50, bs.stream_end_position)
    self.assertEqual(False, bs.stream_exhausted)
    self.assertEqual(self.value[0:50], bs.read(50))
    self.assertEqual(False, bs.stream_exhausted)
    self.assertEqual('', bs.read(0))
    self.assertEqual('', bs.read(100))

  def testExhaustedStream(self):
    bs = buffered_stream.BufferedStream(self.stream, 0, 100)
    self.assertEqual(len(self.value), bs.stream_end_position)
    self.assertEqual(True, bs.stream_exhausted)
    self.assertEqual(self.value, bs.read(100))
    self.assertEqual('', bs.read(0))
    self.assertEqual('', bs.read(100))

  def testArbitraryLengthRead(self):
    bs = buffered_stream.BufferedStream(self.stream, 0, 20)
    with self.assertRaises(exceptions.NotYetImplementedError):
      bs.read()
    with self.assertRaises(exceptions.NotYetImplementedError):
      bs.read(size=-1)


if __name__ == '__main__':
  unittest2.main()
