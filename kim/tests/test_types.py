#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from kim.roles import Role
from kim.mapping import Mapping
from kim.exceptions import ValidationError
from kim.types import (Nested, String, TypeMapper,
                       CollectionTypeMapper, Integer,
                       BaseType, TypedType)


class BaseTypeTests(unittest.TestCase):

    def test_get_value(self):

        my_type = BaseType()
        self.assertEqual(my_type.get_value('foo'), 'foo')

    def test_from_value(self):

        my_type = BaseType()
        self.assertEqual(my_type.from_value('foo'), 'foo')

    def test_validate(self):

        my_type = BaseType()
        self.assertTrue(my_type.validate('foo'), True)


class TypedTypeTests(unittest.TestCase):

    def test_validate_requires_valid(self):
        class MyType(TypedType):

            type_ = list

        my_type = MyType()
        with self.assertRaises(ValidationError):
            self.assertTrue(my_type.validate(''))

    def test_validate(self):

        class MyType(TypedType):

            type_ = list

        self.assertTrue(MyType().validate([]))


class StringTypeTests(unittest.TestCase):

    def test_validate_requires_valid_string_type(self):

        my_type = String()
        with self.assertRaises(ValidationError):
            my_type.validate(0)

    def test_validate_string_type(self):

        my_type = String()
        my_type.validate(u'foo')


class IntegerTypeTests(unittest.TestCase):

    def test_validate_requires_valid_string_type(self):

        my_type = Integer()
        with self.assertRaises(ValidationError):
            my_type.validate('')

    def test_validate_string_type(self):

        my_type = Integer()
        my_type.validate(1)


class TypeMapperTests(unittest.TestCase):

    def test_type_name_correctly_set(self):

        mapped_type = TypeMapper('email', String())
        self.assertEqual(mapped_type.name, 'email')

    def test_source_set_from_type_name_when_not_specified(self):

        mapped_type = TypeMapper('email', String())
        self.assertEqual(mapped_type.source, 'email')

    def test_set_custom_source_param(self):

        mapped_type = TypeMapper('email', String(), source='email_address')
        self.assertEqual(mapped_type.source, 'email_address')

    def test_get_value(self):

        mapped_type = TypeMapper('email', String(), source='email_address')
        self.assertEqual(mapped_type.get_value('foo'), 'foo')

    def test_from_value(self):

        mapped_type = TypeMapper('email', String(), source='email_address')
        self.assertEqual(mapped_type.from_value('foo'), 'foo')

    def test_validate_raises_error_when_required_and_value_null(self):

        mapped_type = TypeMapper('email', String(),
                                 source='email_address',
                                 required=True)
        with self.assertRaises(ValidationError):
            mapped_type.validate('')

    def test_validate_not_allow_none(self):
        mapped_type = TypeMapper('email', String(),
                                 source='email_address',
                                 allow_none=False)

        with self.assertRaises(ValidationError):
            mapped_type.validate(None)

    def test_validate_mapped_type(self):
        mapped_type = TypeMapper('email', String(),
                                 source='email_address',
                                 required=True,
                                 allow_none=False)

        self.assertTrue(mapped_type.validate('foo'))

    def test_type_mapper_default_overrides_type_default(self):

        mapped_type = TypeMapper('email', String(),
                                 default=123)

        self.assertEqual(mapped_type.default, 123)

    def test_set_allow_none(self):
        mapped_type = TypeMapper('email', String(),
                                 allow_none=False)

        self.assertEqual(mapped_type.allow_none, False)


class CollectionTypeMapperTests(unittest.TestCase):

    def test_get_value(self):

        mct = CollectionTypeMapper('l', Integer())
        self.assertEqual(mct.get_value([1, 2, 3]), [1, 2, 3])

    def test_from_value(self):

        mct = CollectionTypeMapper('l', Integer())
        self.assertEqual(mct.from_value([1, 2, 3]), [1, 2, 3])

    def test_validate_iterates_type(self):

        mct = CollectionTypeMapper('l', Integer())
        with self.assertRaises(ValidationError):
            mct.validate([1, '2', 3])

    def test_required_collection_with_null_value(self):
        mct = CollectionTypeMapper('l', Integer(), required=True)
        with self.assertRaises(ValidationError):
            mct.validate([])

    def test_not_allow_none(self):
        mct = CollectionTypeMapper('l', Integer(), allow_none=False)
        with self.assertRaises(ValidationError):
            mct.validate(None)


class NestedTypeTests(unittest.TestCase):

    def test_nested_requires_valid_mapping_type(self):

        with self.assertRaises(TypeError):
            Nested(mapped=list())

    def test_nested_type_sets_role(self):

        role = Role('foo')
        mapping = Mapping()
        nested = Nested(mapped=mapping, role=role)
        self.assertEqual(nested.role, role)

    def test_nested_type_with_core_mapping_type(self):

        mapping = Mapping()
        nested = Nested(mapped=mapping)
        self.assertEqual(nested.mapping, mapping)

    def test_set_new_mapping_on_nested_type(self):

        mapping = Mapping()
        new_mapping = Mapping()

        nested = Nested(mapped=mapping)
        nested.mapping = new_mapping
        self.assertEqual(nested.mapping, new_mapping)

    def test_get_mapping_with_no_role(self):

        mapping = Mapping()
        nested = Nested(mapped=mapping)
        self.assertEqual(nested.get_mapping(), mapping)

    def test_get_mapping_with_role_set(self):

        name, email = TypeMapper('email', String()), TypeMapper('name', String())

        role = Role('foo', 'name')
        mapping = Mapping(name, email)
        nested = Nested(mapped=mapping, role=role)

        mapped = nested.get_mapping()
        self.assertNotEqual(mapped, mapping)

    def test_get_value(self):

        class Inner(object):

            name = 'foo'
            email = 'bar@bar.com'

        name, email = TypeMapper('email', String()), TypeMapper('name', String())
        mapping = Mapping(name, email)

        nested = Nested(mapped=mapping)
        output = nested.get_value(Inner())
        exp = {
            'name': 'foo',
            'email': 'bar@bar.com'
        }
        self.assertDictEqual(output, exp)

    def test_from_value(self):

        class Inner(object):

            name = 'foo'
            email = 'bar@bar.com'

        name, email = TypeMapper('email', String()), TypeMapper('name', String())
        mapping = Mapping(name, email)

        nested = Nested(mapped=mapping)
        output = nested.from_value(Inner())
        exp = {
            'name': 'foo',
            'email': 'bar@bar.com'
        }
        self.assertDictEqual(output, exp)

    def test_nested_validation_validates_mapped_fields(self):
        pass
