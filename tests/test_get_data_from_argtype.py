import inspect
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../src"))
import clig

from typing import Literal, Sequence


def test_get_data_from_argtype_simple_type():
    action, nargs, argtype, choices = clig.get_data_from_argtype(ascii)
    assert action == "store"
    assert nargs == None
    assert argtype == ascii
    assert choices is None


def test_get_data_from_argtype_Literal():
    action, nargs, argtype, choices = clig.get_data_from_argtype(Literal["option1", "option2"])
    assert action == "store"
    assert nargs == None
    assert argtype == str
    assert choices is not None
    assert set(choices) == set(["option1", "option2"])


def test_get_data_from_argtype_List():
    action, nargs, argtype, choices = clig.get_data_from_argtype(list[str])
    assert action == "store"
    assert nargs == "*"
    assert argtype == str
    assert choices is None


def test_get_data_from_argtype_Sequence():
    action, nargs, argtype, choices = clig.get_data_from_argtype(Sequence[int])
    assert action == "store"
    assert nargs == "*"
    assert argtype == int
    assert choices is None


def test_get_data_from_argtype_Tuple():
    action, nargs, argtype, choices = clig.get_data_from_argtype(tuple[int, int, int])
    assert action == "store"
    assert nargs == 3
    assert argtype == int
    assert choices is None


def test_get_data_from_argtype_Tuple_Ellipsis():
    action, nargs, argtype, choices = clig.get_data_from_argtype(tuple[float, ...])
    assert action == "store"
    assert nargs == "*"
    assert argtype == float
    assert choices is None


def test_get_data_from_argtype_Bool():
    action, nargs, argtype, choices = clig.get_data_from_argtype(bool)
    assert action == "store_true"
    assert nargs == None
    assert argtype == bool
    assert choices is None
