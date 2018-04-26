# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2018 FU Berlin and HAW Hamburg
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
"""

from rest_framework import serializers
from api.models import Application
from api.models import ApplicationInstance
from api.models import Board
from api.models import UserProfile
from api.models import Feedback
from django.contrib.auth.models import User


#TODO: Improve!
class UserSerializer(serializers.ModelSerializer):

    is_dev = serializers.SerializerMethodField()
    location = serializers.CharField(source="userprofile.location", required=False, allow_blank=True)
    company = serializers.CharField(source="userprofile.company", required=False, allow_blank=True)
    gender = serializers.ChoiceField(source="userprofile.gender", required=False, allow_blank=True, choices=UserProfile.GENDER_CHOICES)
    phone_number = serializers.CharField(source="userprofile.phone_number", required=False, allow_blank=True)

    class Meta:
        model = User
        exclude = ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions', 'password')
        read_only_fields = ("username", )

    def get_is_dev(self, obj):
        if(obj.has_perm('has_dev_perm')):
            return True
        return False

    def update(self, instance, validated_data):
        userprofile = instance.userprofile
        userprofile.__dict__.update(validated_data.pop('userprofile'))
        instance.__dict__.update(**validated_data)
        instance.save()
        return instance


class ApplicationInstanceSerializer(serializers.ModelSerializer):
    app_tarball = serializers.FileField()
    application = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ApplicationInstance
        exclude = ('is_public',)


class ApplicationSerializer(serializers.ModelSerializer):
    # author = serializers.PrimaryKeyRelatedField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('download_count',)


class BoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):

    is_active = serializers.HiddenField(default=serializers.CreateOnlyDefault(False))

    class Meta:
        model = User
        exclude = ('is_superuser', 'is_staff', 'groups', 'user_permissions')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
