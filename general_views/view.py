from __future__ import unicode_literals
from django.shortcuts import render

def template_loader(request,template_name):
    return render(request,template_name)
