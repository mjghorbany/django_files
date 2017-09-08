from rest_framework import serializers
from .models import Node,Rel

class NodeSerializer(serializers.ModelSerializer):

    class Meta:
        model=Node

        #fields=('name','att1')
        fields='__all__'

