#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Custom hypothesis test strategies. """
from typing import Dict, Callable, Any

import hypothesis.strategies as st
from hypothesis.strategies import SearchStrategy

# pylint: disable=no-value-for-parameter, protected-access


@st.composite
def recursive_extension_dicts(
    draw: Callable[[SearchStrategy], Any], values: SearchStrategy
) -> Dict[str, Any]:
    """ Returns a strategy for dictionaries to be used in ``st.recursive()``. """
    dictionary: Dict[str, Any] = draw(
        st.dictionaries(keys=st.from_regex(r"[a-zA-Z_-]+"), values=values)
    )
    return dictionary


@st.composite
def settings_dicts(draw: Callable[[SearchStrategy], Any]) -> Dict[str, Any]:
    """ Strategy for settings dicts. """
    settings: Dict[str, Any] = draw(
        st.dictionaries(
            keys=st.from_regex(r"[a-zA-Z_-]+"),
            values=st.recursive(
                base=st.one_of(
                    st.floats(),
                    st.integers(),
                    st.text(st.characters()),
                    st.booleans(),
                    st.lists(st.integers()),
                    st.lists(st.floats()),
                    st.lists(st.text(st.characters())),
                ),
                extend=recursive_extension_dicts,
                max_leaves=4,
            ),
        )
    )
    return settings
