"""Util functions."""

import json
from re import sub

def generate_empty_conf_dict():
    """Generates an empty dictionary according to the conference template."""
    with open("ressources/conference_template.json", "r") as template:
        return json.load(template)

def load_conference(filepath):
    """Loads existing conf data into dictionary."""
    with open(filepath, "r", encoding='utf-8') as f:
        return json.load(f)

def save_conference_data(conf_name, conf_data):
    """Saves the generated conf_data dict to file in the output folder."""
    with open("output/" + conf_name.replace(" ", "").lower() + "_data.json", "w",
              encoding='utf-8') as f:
        json.dump(conf_data, f, ensure_ascii=False)

def basic_string_clean(string):
    """Basic string cleaning."""
    return sub(r'([\n\t]|^\s+|\s+$)', "", string)