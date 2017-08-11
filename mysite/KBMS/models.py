from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Node(models.Model):
    node=models.CharField(max_length=20)
    att1=models.CharField(max_length=20)
    att2 = models.CharField(max_length=20)
    att3 = models.CharField(max_length=20)

    def get_absolute_url(self):
        return reverse('node:detail', kwargs={'pk':self.pk})


    def __str__(self):
        return self.node

