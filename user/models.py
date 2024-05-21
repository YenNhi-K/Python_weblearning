from django.db import models
from django.core.validators import MinLengthValidator

class User(models.Model):
    user_id = models.AutoField(primary_key=True, error_messages="Tên đăng nhập đã tồn tại")  # Sử dụng AutoField để tự động tăng user_id
    username = models.CharField(max_length=50)  # unique=True để đảm bảo giá trị username là duy nhất
    password = models.CharField(max_length=20, validators=[MinLengthValidator(8)])

    def __str__(self):
        return self.username

    