# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import yaml
from ozun.settings import PROJECT_DIR

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
    with open(PROJECT_DIR+'/equipments/tests/{}'.format(file_name),'r' ,encoding = 'utf-8') as file:
        file_str = file.read()
        data = yaml.load_all( strip_invalid(file_str) )
    return data
    
def get_test_image_path():
    return PROJECT_DIR+'/equipments/tests/test_image.jpg'