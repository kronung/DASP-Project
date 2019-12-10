"""Util functions."""

import json

def build_conference_dict(filepath, conf_name):
    with open(filepath, "r", encoding='utf-8') as f:
        return json.load(f)[conf_name]

