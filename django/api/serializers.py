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

import hashlib
import tarfile


#TODO: Improve!
class UserSerializer(serializers.ModelSerializer):

    is_dev = serializers.SerializerMethodField()
    location = serializers.CharField(source='userprofile.location', required=False, allow_blank=True)
    company = serializers.CharField(source='userprofile.company', required=False, allow_blank=True)
    gender = serializers.ChoiceField(source='userprofile.gender', required=False, allow_blank=True, choices=UserProfile.GENDER_CHOICES)
    phone_number = serializers.CharField(source='userprofile.phone_number', required=False, allow_blank=True)

    class Meta:
        model = User
        exclude = ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions', 'password')
        read_only_fields = ('username', )

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
        exclude = ('is_public', 'app_tarball_md5')

    def validate(self, data):

        try:
            application_id = self.context['application_id']

        except KeyError:
            application_id = -1

        message_file_duplicate = 'This file was already uploaded.'

        file = data['app_tarball']
        tarball_md5 = _md5_of_tar(file)

        # application_id "-1" is used if application is being created and has no id already
        #   -> just accept tarball because there cant be the same tarball if there is nothing
        if application_id != -1 and ApplicationInstance.objects.filter(application=application_id, app_tarball_md5=tarball_md5):
            raise serializers.ValidationError(message_file_duplicate)

        data['app_tarball_md5'] = tarball_md5

        return data

    def validate_app_tarball(self, data):

        message_file_format = 'Invalid tar.gz file. Ensure the Makefile is in the root of the compressed file.'

        try:
            tar = tarfile.open(fileobj=data, mode='r')

        except:
            raise serializers.ValidationError(message_file_format)

        if './Makefile' not in tar.getnames() and 'Makefile' not in tar.getnames():
            raise serializers.ValidationError(message_file_format)

        return data


class ApplicationSerializer(serializers.ModelSerializer):
    # author = serializers.PrimaryKeyRelatedField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('download_count', 'source')


class BoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):

    is_active = serializers.HiddenField(default=serializers.CreateOnlyDefault(True))

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


def _md5_of_tar(file):
    """ calculate hash of archive over the content of all included files within the archive """

    hash_md5 = hashlib.md5()

    file.open()
    tar = tarfile.open(fileobj=file)

    for tarinfo in tar:

        if tarinfo.isfile():

            f = tar.extractfile(tarinfo)
            content = f.read()

            hash_md5.update(content)

    tar.close()

    return hash_md5.hexdigest()
