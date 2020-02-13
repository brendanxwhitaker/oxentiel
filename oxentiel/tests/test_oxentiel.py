#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Test that the ``Oxentiel`` class loads dictionaries correctly. """
from typing import Dict, Any

from hypothesis import given

from oxentiel import Oxentiel
from oxentiel.tests import strategies

# pylint: disable=no-value-for-parameter


@given(strategies.settings_dicts())
def test_ox_adds_all_keys_from_nested_dicts(settings: Dict[str, Any]) -> None:
    """ Test that all keys are added when the dictionary is nested. """
    ox = Oxentiel(settings)

    def check_keys(mapping: Dict[str, Any], ox: Oxentiel) -> None:
        """ Recursively add all keys from a nested dictionary. """
        for key, value in mapping.items():
            if isinstance(value, dict):
                check_keys(value, getattr(ox, key))
            assert key in ox.keys()

    check_keys(settings, ox)


@given(strategies.settings_dicts())
def test_ox_attributes_get_set(settings: Dict[str, Any]) -> None:
    """ Test that all keys are set as attributes. """
    ox = Oxentiel(settings)

    def check_attributes(mapping: Dict[str, Any], ox: Oxentiel) -> None:
        """ Recursively add all keys from a nested dictionary. """
        for key, value in mapping.items():
            if isinstance(value, dict):
                check_attributes(value, getattr(ox, key))
            assert hasattr(ox, key)

    check_attributes(settings, ox)


def test_ox_settings_passed_by_value() -> None:
    """ Test that modifying ``Oxentiel.settings`` doesn't change the argument dict. """
    settings = {"key": {"subkey": [1, 2]}}
    ox = Oxentiel(settings)
    settings["key"]["subkey"].append(3)
    assert 3 not in ox.key.subkey


@given(strategies.settings_dicts())
def test_ox_repr_prints_everything(settings: Dict[str, Any]) -> None:
    """ Test that every key appears in the string representation. """
    ox_repr = repr(Oxentiel(settings))
    print(ox_repr)
    for key in settings:
        assert repr(key) in ox_repr
