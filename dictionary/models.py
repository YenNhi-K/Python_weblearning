from django.db import models
from english_test.models import Test
# Create your models here.
class Dictionary(models.Model):
    dict_id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=200)
    meaning = models.CharField(max_length=200)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)