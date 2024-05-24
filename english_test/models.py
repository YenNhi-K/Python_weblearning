from django.db import models
from user.models import User

# Create your models here.
class Test(models.Model):
    test_id = models.AutoField(primary_key=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=True)
    number_of_words = models.IntegerField(default=0)
    topic = models.CharField(max_length=50, default='')

class History(models.Model):
    id = models.AutoField(primary_key=True) 
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.IntegerField(default=0)
    number_of_questions = models.IntegerField(default=0)
    type = models.BooleanField(default=False)
    test_time = models.DateTimeField(auto_now_add=True)
    