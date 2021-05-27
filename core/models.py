from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class DataSet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, null=True, blank=True)

    cols_name = models.CharField(max_length=2000, null=True, blank=True)
    cols_type = models.CharField(max_length=2000, null=True, blank=True)
    cols_desc = models.CharField(max_length=2000, null=True, blank=True)

    graphsx = models.CharField(max_length=2000, null=True, blank=True)
    graphsy = models.CharField(max_length=2000, null=True, blank=True)

    reg_cols = models.CharField(max_length=2000, null=True, blank=True, default="")
    
    clas_cols = models.CharField(max_length=2000, null=True, blank=True, default="")

    price = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.CharField(max_length=2000, null=True, blank=True)

    reg_res = models.JSONField(null=True, blank=True)
    clas_res = models.JSONField(null=True, blank=True)

    filename = models.CharField(max_length=1000)
    def __str__(self):
        return self.title
    