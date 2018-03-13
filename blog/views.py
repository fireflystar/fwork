from django.shortcuts import render,redirect
from django.db.models import Q 
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from . import models


from django import forms
from django.forms import widgets
from django.forms import fields


class blogForm(forms.Form):
    writer = fields.CharField(
        error_messages={'required': '作者不能为空.'},      
        label="作者",
        required=True,
        )

    content = fields.CharField(
        error_messages={'required': '内容不能为空.'},
        widget=widgets.Textarea(attrs={'cols': 80, 'rows': 4}),
        label="通知正文",
        required=True,
        )


# Create your views here.
def blog(request):
    msg = list()
    if request.method == "GET":
        bf = blogForm()#POST请求以外的情况，给uf变量赋值
        blog_list = models.blog.objects.order_by('-ctime')

        return render(request,"blogshow.html",{
            'bf':bf,
            'blog_list':blog_list,
            'msg':msg
            })



    if request.method == "POST":
        bf = blogForm(request.POST)
        if bf.is_valid():
            writer = bf.cleaned_data['writer']
            content = bf.cleaned_data['content']

            if models.blog.objects.filter(content=content):
                msg.append("内容已经存在了，请不要重复输入")
            else:
                models.blog.objects.create(
                    writer=writer,
                    content=content
                    )
        blog_list = models.blog.objects.order_by('-ctime')
        
        bf = blogForm()
        return render(request,"blogshow.html",{
            'bf':bf,
            'blog_list':blog_list,
            'msg':msg
            })