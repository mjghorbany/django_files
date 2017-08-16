from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Node(models.Model):
    ini_node=models.CharField(max_length=20)
    att1=models.CharField(max_length=20)
    att2 = models.CharField(max_length=20)
    att3 = models.CharField(max_length=20)

    def get_absolute_url(self):
        return reverse('KBMS:detail', kwargs={'pk':self.pk})


    def __str__(self):
        return self.att1 + ' + ' + self.att2

class Rel(models.Model):
	rel_start=models.ForeignKey(Node,related_name='start_node',on_delete=models.CASCADE)
    rel_end = models.ForeignKey(Node,related_name='end_node',on_delete=models.CASCADE)
	rel_type=models.CharField(max_length=10)
	rel_title=models.CharField(max_length=250)
	is_favorite=models.BooleanField(default=False)

	def __str__(self):
		return self.rel_title+ "." + self.rel_type