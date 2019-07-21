# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin, messages
from . import models
from .models import LessonTree
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory , MoveNodeForm , _get_exclude_for_model
from .exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseBadRequest

def clean_lesson_tree(ref_node , content , position ):
    if position == 'sibling':
        check_nods = ref_node.get_siblings()
        level = ref_node.depth 
                    
    if position == 'child':
        check_nods = ref_node.get_children()
        level = ref_node.depth + 1 # content is child of ref node so it level is ref_node level + 1 
        
        if level > 4 :
            raise ValidationError(_('can not add child for "Topic" type content'))
    
    if content.getNumberByType(content.type) != level:
        raise ValidationError(_('can not add content to this depth'))
    
    for node in check_nods:
        if node.content == content:
            raise ValidationError(_('content already exist in selected branch') )


class LssonTreeForm(MoveNodeForm):
    def clean(self):
        ref_node_id = self.cleaned_data['_ref_node_id']
        content = self.cleaned_data['content']
        if self.cleaned_data['_position'] == 'sorted-child':
            pos = 'child'
        if self.cleaned_data['_position'] == 'sorted-sibling':
            pos = 'sibling'
        
        if ref_node_id == 0: # if it is root
            ref_node = LessonTree().get_root_nodes()[0]
            pos = 'sibling'
        else:
            ref_node = LessonTree.objects.get(id = ref_node_id)
        

        clean_lesson_tree( ref_node , content , pos )

        return self.cleaned_data
        
    class Meta:
        exclude = _get_exclude_for_model(LessonTree,None)
        model = LessonTree


class MyAdmin(TreeAdmin):
    # clean data in move , saving data in move is diffrent with form
    # so we should check it again 
    def try_to_move_node(self, as_child, node, pos, request, target):
        if as_child:
            position = 'child'
        else:
            position = 'sibling'
        try:
            clean_lesson_tree(target,node.content,position)
        except ValidationError as e:
            messages.error(request,
                _('Exception raised while moving node: %s') % _(e.message))
            return HttpResponseBadRequest('Exception raised during move')
        
        return super().try_to_move_node(as_child, node, pos, request, target)

    form = LssonTreeForm

admin.site.register(LessonTree,MyAdmin)
admin.site.register(models.TreeContent)
admin.site.register(models.FeedBack)
