"""Util functions."""

import json
from re import sub

def build_conference_dict(filepath, conf_name):
    with open(filepath, "r", encoding='utf-8') as f:
        return json.load(f)[conf_name]

def basic_string_clean(string):
    return sub(r'([\n\t]|^\s+|\s+$)', "", string)