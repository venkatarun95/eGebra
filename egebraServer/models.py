from django.db import models
from django.contrib.auth.models import User

maxSymbolicObjectLength = 2048
# Create your models here.
class Notebooks(models.Model):
	owner = models.ForeignKey(User)

class SymbolicObjects(models.Model):
	pklObj = models.CharField(max_length = maxSymbolicObjectLength)
	notebook = models.ForeignKey('Notebooks')