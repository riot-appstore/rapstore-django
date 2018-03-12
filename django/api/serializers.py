from rest_framework import serializers
from uploader.models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        exclude = ('app_tarball',)
