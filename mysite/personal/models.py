from django.db import models

# Create your models here.
class Triple(models.Model):
    node1=models.CharField(max_length=20)
    edge=models.TextField()
    node2=models.CharField(max_length=20)

    def __str__(self):
        return self.node1
