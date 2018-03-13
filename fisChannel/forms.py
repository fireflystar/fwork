from django import forms
from django.forms import widgets
from django.forms import fields

class UserForm(forms.Form):
    username = fields.CharField(label="帐号", max_length=254,required=True,
        error_messages={'required':"帐号不能为空"})
    password = fields.CharField(label="密码", widget=forms.PasswordInput,required=True,
        error_messages={'required':"帐号不能为空"})


class tijiaoForm(forms.Form):
    tongdao_name = fields.CharField(
        error_messages={'required': '通道名不能为空.'},
        required=True,
        label="通道名",
        )
    
    ip = fields.CharField(
        required=False,
        label="ip地址",
        )

    email_list = fields.CharField(
        widget=widgets.Textarea(),
        label="邮箱列表",
        required=False,
        )

    factory = fields.CharField(
        required=False,
        label="厂",
        )

    department = fields.CharField(
        required=False,
        label="部门",
        )

