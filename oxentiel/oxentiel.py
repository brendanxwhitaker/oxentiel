#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Converts settings dictionary into a configuration object. """
# NOTE: StackOverflow reference:
# /questions/42272335/how-to-make-a-class-which-has-getattr-properly-pickable
import copy
from typing import Dict, Any

from oxentiel import pprint


class Oxentiel(dict):
    """
    Configuration object.

    Parameters
    ----------
    settings : ``Dict[str, Any]``.
    """

    def __init__(self, settings: Dict[str, Any], mutable: bool = False):

        # Set any attributes here - before initialisation (they remain normal attrs).
        self.settings: Dict[str, Any] = copy.deepcopy(settings)
        self.mutable: bool = mutable
        dict.__init__(self, settings)

        # Add all key-value pairs.
        for key, value in self.settings.items():
            if isinstance(value, dict):
                value = Oxentiel(value)
            setattr(self, key, value)

        # After initialization, setting attributes is the same as setting an item.
        self.__initialized = True

    def __getattr__(self, item: str) -> Any:
        """ Maps values to attrs. Only called if there's no attr with name ``item``. """
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, item: str, value: Any) -> None:
        """ Maps attributes to values. Only if we are initialised. """
        # This test allows attributes to be set in the ``__init__()`` method.
        if "_Oxentiel__initialized" not in self.__dict__:
            dict.__setattr__(self, item, value)
        # Any normal attributes are handled normally.
        elif not self.mutable:
            raise AttributeError(
                "Can't assign attribute. 'Oxentiel' object is immutable."
            )
        elif isinstance(value, Oxentiel):
            raise AttributeError(
                "Can't assign object of type 'Oxentiel' as an attribute."
            )
        elif item in self.__dict__:
            dict.__setattr__(self, item, value)
            self.settings[item] = value
        else:
            self.__setitem__(item, value)
            self.settings[item] = value

    def __repr__(self) -> str:
        """ Return string representation of 'Oxentiel' object. """
        rep: str = pprint.pformat(self.settings, sort_dicts=False) # type: ignore
        return rep
