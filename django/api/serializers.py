from rest_framework import serializers
from api.models import Application
from api.models import Board
from django.contrib.auth.models import User

class ApplicationSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Application
        exclude = ('app_tarball',)

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    is_dev = serializers.SerializerMethodField()
    location = serializers.CharField(source="userprofile.location", required=False)
    company = serializers.CharField(source="userprofile.company", required=False)
    gender = serializers.CharField(source="userprofile.gender", required=False)
    phone_number = serializers.CharField(source="userprofile.phone_number", required=False)

    class Meta:
        model = User
        exclude = ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')
        extra_kwargs = {'password': {'write_only': True}}

    def get_is_dev(self, obj):
        if(obj.has_perm('has_dev_perm')):
            return True
        return False

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user
