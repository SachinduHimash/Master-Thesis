from rest_framework import serializers
from .models import Convo

class ConvoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convo
        fields = '__all__'