# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import yaml
from studylab.settings import PROJECT_DIR
from core.models import Location

def strip_invalid(s):
    res = ''
    for x in s:
        if yaml.reader.Reader.NON_PRINTABLE.match(x):
            res += '\\x{:x}'.format(ord(x) )
            ord()
            continue
        res += x
    return res

def create_documents(file_name):
    with open(PROJECT_DIR+'/equipments/tests/{}'.format(file_name),'r') as file:
        file_str = file.read()
        data = yaml.load_all( strip_invalid(file_str) )
    return data

def embed_test_locations():
    data = next(create_documents('locations.yaml'))
    for key in data:
        Location().create_by_path(data[key])
    
def get_test_image_path():
    return PROJECT_DIR+'/equipments/tests/test_image.jpg'