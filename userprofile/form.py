from django import forms

from django.contrib.auth.models import User
from .models import Profile

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.CharField(required=True)
    password = forms.CharField(required=True,
                               min_length= 8,
                               )
    password2 = forms.CharField(required=True,
                                min_length= 8,
                               )


    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError('密码输入不一致，请重新输入。')

class ProfileForm(forms.ModelForm):
    class Meta:
        model= Profile
        fields = ("name", "birth", "phone", "avatar", "intro", "school", "profession", "education", "skill", "address", "career", "homepage")
