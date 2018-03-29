from rest_framework import serializers
from api.models import Application
from api.models import Board
from django.contrib.auth.models import User

class ApplicationSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Application
        fields = '__all__'

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'
