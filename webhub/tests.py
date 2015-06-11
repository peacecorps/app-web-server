from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from webhub.models import Pcuser, Post

class PostAPITestCase(APITestCase):

    def setUp(self):

        u1 = User.objects.create_superuser(username='admin', password='password', email='')
        u1.save()

        o1 = Pcuser(user = u1)
        o1.save()

        p1 = Post(owner = o1,
                title_post = "Test",
                description_post = "Tester")
        p1.save()

    def test_get_posts(self):
        
        self.client.login(username='admin', password='password')
        p1 = Post.objects.all().first()
        post_id = str(p1.id)
        #name of viewset is post-detail
        url = reverse('post-detail', args=[post_id])
        response = self.client.get(url)
        print response
