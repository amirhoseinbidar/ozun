from __future__ import unicode_literals
from django.shortcuts import render
from django.http import Http404

def template_loader(request,template_name):
    return render(request,template_name)

#method spliter  splite betwine diffrent  request methods
def method_splitter(request, GET=None, POST=None , **kwargs):
    if request.method == 'GET' and GET is not None:
        return GET(request,**kwargs)
        
       
    elif request.method == 'POST' and POST is not None:
        return POST(request,**kwargs)
    else:
        raise Http404