from django import forms

from volunteer.models import Department


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': ''}),
                               error_messages={'required': '用户名不能为空', 'min_length': '用户名最少为3个字符',
                                               'max_length': '用户名最不超过为20个字符'}, )
    password = forms.CharField(label="密码", max_length=20,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': ''}))
    password1 = forms.CharField(label="密码", max_length=20,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
    password2 = forms.CharField(label="确认密码", max_length=20,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
