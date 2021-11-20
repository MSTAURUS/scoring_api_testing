#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tarantool
import unittest
import warnings

import api
from tests.utils import cases
from storage import TarantoolConnection


class TestSuite_Tarantool(unittest.TestCase):
    def setUp(self):
        self.host = "localhost"
        self.port = 3301
        self.user = "username"
        self.password = "password"
        self.srv = TarantoolConnection()

    def test_get_connection(self):
        with self.assertRaises(ValueError):
            self.srv.get_connection()

    def test_set(self):
        """Testing VALID Tarantool.set"""
        con = self.srv.get_connection()
        con.set('{"1": ["books", "hi-tech"]} ')

    def test_invalid_set(self):
        """Testing INVALID Tarantool.set"""
        con = self.srv.get_connection()
        with self.assertRaises(ValueError):
            con.set("qqqqq ")

    def test_get(self):
        """Testing VALID Tarantool.get"""
        self.srv.get("1")

    def test_invalid_get(self):
        """Testing INVALID Tarantool.get"""
        with self.assertRaises(ValueError):
            self.srv.get("-1")


if __name__ == "__main__":
    unittest.main()
