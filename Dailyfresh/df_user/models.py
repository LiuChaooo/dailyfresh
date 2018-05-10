# -*- coding: utf-8 -*-
# Create your models here.
from __future__ import unicode_literals
from django.db import models
class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=30)


