from django import forms
from captcha.fields import CaptchaField

from .models import Userprofile


class UploadImageForm(forms.ModelForm):
    """
    上传图片
    """
    class Meta:
        model = Userprofile
        fields = ["image"]


class Login_form(forms.Form):
    """
    登陆表单验证
    """
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    """
    图片验证码验证表单
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误！"})


class ForgetForm(forms.Form):
    """
    忘记密码验证表单
    """
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误！"})

class ModifyForm(forms.Form):
    """
    修改密码验证表单
    """
    password1 = forms.CharField(required=True,min_length=5)
    password2 = forms.CharField(required=True,min_length=5)
