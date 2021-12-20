#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tarantool
import unittest
import warnings

import api
from tests.utils import cases
from storage import TarantoolConnection

HOST = os.environ.get("TARANTOOL_HOST", "")
PORT = os.environ.get("TARANTOOL_PORT", "")
USERNAME = os.environ.get("TARANTOOL_USERNAME", "")
PASSWORD = os.environ.get("TARANTOOL_PWD", "")

SKIPING_TEST_FLG = True if HOST == '' or PORT == '' else False


@unittest.skipIf(SKIPING_TEST_FLG, "No DB connection params")
class TestSuite_Tarantool(unittest.TestCase):
    def setUp(self):
        self.host = HOST
        self.port = PORT
        self.user = USERNAME
        self.password = PASSWORD
        self.srv = TarantoolConnection(
            host=self.host, port=self.port, user=self.user, password=self.password
        )

    def test_get_connection(self):
        with self.assertRaises(ValueError):
            self.srv.get_connection()

    def test_set(self):
        """Testing VALID Tarantool.set"""
        self.assertTrue(self.srv.set('{"1": ["books", "hi-tech"]} '))

    def test_invalid_set(self):
        """Testing INVALID Tarantool.set"""
        with self.assertRaises(ValueError):
            self.srv.set("qqqqq ")

    def test_get(self):
        """Testing VALID Tarantool.get"""
        self.assertIsNotNone(self.srv.get("1"))

    def test_invalid_get(self):
        """Testing INVALID Tarantool.get"""
        with self.assertRaises(ValueError):
            self.srv.get("-1")


if __name__ == "__main__":
    unittest.main()
