from django.db import models

# Create your models here.
class Block_List(models.Model):
 ip_address=models.GenericIPAddressField(unique=True,null=True)
 
 def __str__(self):
  return self.ip_address