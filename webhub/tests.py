from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APITestCase
from webhub.models import Pcuser, Post
from webhub.serializers import PostSerializer

class PostAPITestCase(APITestCase):

    def setUp(self):

        u1 = User.objects.create_superuser(username='admin', password='password', email='')
        u1.save()

        o1 = Pcuser(user = u1)
        o1.save()

        p1 = Post(owner = o1,
                title_post = "Title 1",
                description_post = "Description 1")

        p2 = Post(owner = o1,
                title_post = "Title 2",
                description_post = "Description 2")

        p3 = Post(owner = o1,
                title_post = "Title 3",
                description_post = "Description 3")

        p1.save()
        p2.save()
        p3.save()

    def test_positive_cases(self):
        
        self.client.login(username='admin', password='password')
        post_list = Post.objects.all().order_by('id')

        for post in post_list:
            post_id = str(post.id)

            #name of viewset is post-detail
            url = reverse('post-detail', args=[post_id])
            response = self.client.get(url)

            serializer = PostSerializer(post)
            content = JSONRenderer().render(serializer.data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.accepted_media_type, "application/json")
            self.assertEqual(response.render().content, content)
