from django.core.exceptions import ObjectDoesNotExist
from malaria.models import Post, RevPost


def delete_post_by_id(post_id):

    is_deleted = False
    try:
        post = Post.objects.get(pk=post_id)
        post.delete()
        is_deleted = True
    except ObjectDoesNotExist:
        pass

    return is_deleted


def get_post_by_id(post_id):

    post = None
    try:
        post = Post.objects.get(pk=post_id)
    except ObjectDoesNotExist:
        pass

    return post


def get_revpost_of_owner(post_id):

    revpost = None
    try:
        revpost = RevPost.objects.filter(owner_rev_post_id=post_id)
    except ObjectDoesNotExist:
        pass

    return revpost
