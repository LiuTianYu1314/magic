from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

class SimpleUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=16,
        widget=forms.TextInput(attrs={'placeholder': '请输入不超过16位的数字或字母'}),
        help_text='请输入不超过16位的数字或字母组合'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '请输入不超过16位的数字或字母'}),
        help_text='请输入不超过16位的数字或字母组合'
    )
    password2 = None  # 移除密码确认字段

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9]{1,16}$', username):
            raise forms.ValidationError('用户名必须是1-16位数字或字母的组合')
        return username

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if not re.match(r'^[a-zA-Z0-9]{1,16}$', password):
            raise forms.ValidationError('密码必须是1-16位数字或字母的组合')
        return password

    class Meta:
        model = User
        fields = ('username',)