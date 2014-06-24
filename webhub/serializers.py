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
        fields = ('owner', 'title_post', 'description_post', 'link_post', 'created','updated','id','image_post','imageobj_post')
        
        
class RevPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevPost
        fields = ('owner_rev_post', 'owner_rev', 'title_post_rev', 'description_post_rev', 'link_post_rev', 'created','id','title_change','description_change','link_change')
        

    
  