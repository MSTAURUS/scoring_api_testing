#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools
import unittest

import api
from tests.utils import cases


class TestSuite(unittest.TestCase):
    def setUp(self):
        self.context = {}
        self.headers = {}
        self.store = None

    def get_response(self, request):
        return api.method_handler(
            {"body": request, "headers": self.headers}, self.context, self.store
        )

    def test_empty_request(self):
        _, code = self.get_response({})
        self.assertEqual(api.INVALID_REQUEST, code)


class TestCharField(unittest.TestCase):
    @cases(["", "Test", "/test", "\\test"])
    def test_valid_value(self, val):
        """Testing VALID CharField"""
        with self.assertTrue:
            api.CharField(required=False, nullable=True).validate(value=val)

    @cases([1, -1])
    def test_invalid_value(self, val):
        """Testing INVALID CharField"""
        with self.assertRaises(ValueError):
            api.CharField(required=False, nullable=True).validate(value=val)


class TestArgumentsField(unittest.TestCase):
    @cases([{}, {"key": "val"}])
    def test_valid_value(self, val):
        """Testing VALID ArgumentsField"""
        with self.assertTrue:
            api.ArgumentsField(required=False, nullable=True).validate(value=val)

    @cases([True, -1, "", ["key", "val"]])
    def test_invalid_value(self, val):
        """Testing INVALID ArgumentsField"""
        with self.assertRaises(ValueError):
            api.ArgumentsField(required=False, nullable=True).validate(value=val)


class TestEmailField(unittest.TestCase):
    @cases(["a@b.ru", "e@mail.ru"])
    def test_valid_value(self, val):
        """Testing VALID EmailField"""
        with self.assertTrue:
            api.EmailField(required=False, nullable=True).validate(value=val)

    @cases(["test_user", 1, 0.1])
    def test_invalid_value(self, val):
        """Testing INVALID EmailField"""
        with self.assertRaises(ValueError):
            api.EmailField(required=False, nullable=True).validate(value=val)


class TestPhoneField(unittest.TestCase):
    @cases(["79123457890", 70987654321])
    def test_valid_value(self, val):
        """Testing VALID PhoneField"""
        with self.assertTrue:
            api.PhoneField(required=False, nullable=True).validate(value=val)

    @cases(["81234567890", 80987654321, 709876543211, -1])
    def test_invalid_value(self, val):
        """Testing INVALID PhoneField"""
        with self.assertRaises(ValueError):
            api.PhoneField(required=False, nullable=True).validate(value=val)


class TestDateField(unittest.TestCase):
    @cases(["01.05.1987"])
    def test_valid_value(self, val):
        """Testing VALID DateField"""
        with self.assertTrue:
            api.DateField(required=False, nullable=True).validate(value=val)

    @cases(["01-01-2000", "01.01.00", "01.18.2000", "33.01.2000", 1012000])
    def test_invalid_value(self, val):
        """Testing INVALID DateField"""
        with self.assertRaises(ValueError):
            api.DateField(required=False, nullable=True).validate(value=val)


class TestBirthDayField(unittest.TestCase):
    @cases(["01.05.1987"])
    def test_valid_value(self, val):
        """Testing VALID BirthDayField"""
        with self.assertTrue:
            api.BirthDayField(required=False, nullable=True).validate(value=val)

    @cases(["01.01.1917"])
    def test_invalid_value(self, val):
        """Testing INVALID BirthDayField"""
        with self.assertRaises(ValueError):
            api.BirthDayField(required=False, nullable=True).validate(value=val)


class TestGenderField(unittest.TestCase):
    @cases([0, 1, 2])
    def test_valid_value(self, val):
        """Testing VALID GenderField"""
        with self.assertTrue:
            api.GenderField(required=False, nullable=True).validate(val=val)

    @cases(["", "q", -1, 3])
    def test_invalid_value(self, val):
        """Testing INVALID GenderField"""
        with self.assertRaises(ValueError):
            api.GenderField(required=False, nullable=True).validate(val=val)


class ClientIDsField(unittest.TestCase):
    @cases([[0, 1], [1]])
    def test_valid_value(self, val):
        """Testing VALID ClientIDsField"""
        with self.assertTrue:
            api.ClientIDsField(required=False, nullable=True).validate(val=val)

    @cases([[], {"key": 1}, "text", [1, "a"], [1.1, 2.2], [[1, 2], [3, 4]]])
    def test_invalid_value(self, val):
        """Testing INVALID ClientIDsField"""
        with self.assertRaises(ValueError):
            api.ClientIDsField(required=False, nullable=True).validate(val=val)


if __name__ == "__main__":
    unittest.main()
