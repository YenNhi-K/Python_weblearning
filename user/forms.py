from django import forms
from .models import User
class UserRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 're-password', 'placeholder': 'Xác nhận mật khẩu'}), label="Confirm password *")
    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': 'Email/Username *',
            'password': 'Password *',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'username', 'placeholder': 'Nhập username hoặc email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password', 'placeholder': 'Nhập mật khẩu'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            self.add_error('username', "Username đã tồn tại")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Password không trùng khớp")
        return cleaned_data

class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': 'Email/Username *',
            'password': 'Password *',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'username', 'placeholder': 'Nhập username hoặc email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password', 'placeholder': 'Nhập mật khẩu'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data.get("password")
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            self.add_error('username', "Username không tồn tại")
        elif not User.objects.filter(username=username,password=password).exists():
            self.add_error('password', "Password không đúng")
        return cleaned_data

