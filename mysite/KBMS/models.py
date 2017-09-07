from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, User

# Create your models here.
class Node(models.Model):

    name = models.CharField(max_length=20)
    att1=models.CharField(max_length=20)
    att2 = models.CharField(max_length=20)
    att3 = models.CharField(max_length=20)

    def get_absolute_url(self):
        return reverse('KBMS:detail', kwargs={'pk':self.pk})


    def __str__(self):
        return self.name

class Rel(models.Model):
    rel_start=models.ForeignKey(Node,related_name='start_node',on_delete=models.CASCADE)
    rel_end = models.ForeignKey(Node,related_name='end_node',on_delete=models.CASCADE)
    rel_type=models.CharField(max_length=10)
    rel_title=models.CharField(max_length=250)
    is_favorite=models.BooleanField(default=False)

    def __str__(self):
        return self.rel_title+ "." + self.rel_type

class Ontology(models.Model):
    user = models.ForeignKey(User, default=1)
    domain = models.CharField(max_length=250)
    ontology_title = models.CharField(max_length=500)
    description = models.CharField(max_length=400)
    ontology_logo = models.FileField()
    is_available = models.BooleanField(default=False)

    def __str__(self):
        return self.ontology_title + ' - ' + self.domain