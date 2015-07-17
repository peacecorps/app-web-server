from django.forms import ModelForm
from malaria.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title_post', 'description_post']
