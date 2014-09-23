from django.db import models

# Create your models here.

class Pmid(models.Model):
    pubmed_id=models.CharField(max_length=20)
    date_added=models.DateField(auto_now_add=True,auto_now=True)
    
class BrainRegion(models.Model):
    name=models.CharField(max_length=100)
    query=models.CharField(max_length=255)
    atlasregion=models.BooleanField(default=False)
