from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
 




class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    display_name=models.CharField(max_length=250)

    # DisplayField = ['username','email']



    class Meta:
        db_table= "customuser"


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)

   


    DisplayField = ['id','title','description','status','user_id']