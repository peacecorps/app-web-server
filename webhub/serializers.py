from django.contrib.auth.models import User
from webhub.models import *

from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class PcuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pcuser
        fields = ('user', 'location', 'phone', 'gender','id')
        
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('owner', 'title_post', 'description_post', 'created','updated','id')