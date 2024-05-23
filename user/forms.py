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
class UserChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'current-password', 'placeholder': 'Nhập mật khẩu hiện tại'}), label="Current password *")
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'new-password', 'placeholder': 'Nhập mật khẩu mới'}), label="New password *")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 're-password', 'placeholder': 'Xác nhận mật khẩu mới'}), label="Confirm new password *")
    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', "Password không trùng khớp")
        if len(new_password) < 8 or len(new_password) > 20:
            self.add_error('new_password', "Password từ 8 đến 20 kí tự")
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

