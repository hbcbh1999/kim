#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from kim.roles import Role, create_mapping_from_role, whitelist, blacklist
from kim.mapping import Mapping
from kim import types
from kim.type_mapper import TypeMapper


class MyCustomMapping(Mapping):
    pass


class CustomRole(Role):
    pass


class RoleTests(unittest.TestCase):

    def test_field_names_correctly_set(self):

        role = Role('field_a', 'field_b')
        self.assertEqual(role.field_names, ('field_a', 'field_b'))

    def test_set_whitelist_option(self):

        role = Role(whitelist=False)
        self.assertFalse(role.whitelist)

    def test_membership_for_whitelist_role(self):

        role = Role('users', 'email', whitelist=True)
        self.assertTrue(role.membership('email'))
        self.assertFalse(role.membership('name'))

    def test_membership_for_blacklist_role(self):

        role = Role('users', 'email', whitelist=False)
        self.assertFalse(role.membership('email'))
        self.assertTrue(role.membership('name'))

    def test_create_role_mapping_uses_mapping_type(self):

        mapping = MyCustomMapping('users', TypeMapper('name', types.String()))
        role = Role('name')
        mapped = create_mapping_from_role(role, mapping)
        self.assertIsInstance(mapped, MyCustomMapping)

    def test_create_mapping_from_role(self):
        name = TypeMapper('name', types.String())
        email = TypeMapper('email', types.String())

        mapping = MyCustomMapping('users',
                                  name,
                                  email)
        role = Role('name')

        mapped = create_mapping_from_role(role, mapping)
        self.assertIn(name, mapped.fields)
        self.assertNotIn(email, mapped.fields)

    def test_whitelist_utility_function(self):

        role = whitelist('name')
        self.assertEqual(role.field_names, ('name',))
        self.assertTrue(role.whitelist)

    def test_blacklist_utility_funcation(self):

        role = blacklist('name')
        self.assertEqual(role.field_names, ('name',))
        self.assertFalse(role.whitelist)

    def test_create_role_with_custom_base(self):

        role = whitelist('bar', role_base=CustomRole)
        self.assertIsInstance(role, CustomRole)
