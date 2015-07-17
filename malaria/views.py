from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from malaria.forms import PostForm
from malaria.models import Post, RevPost
from malaria.services import delete_post_by_id, get_post_by_id, get_revpost_of_owner
from webhub.checker import check
from webhub.models import Pcuser
from webhub.serializers import PostSerializer, RevPostSerializer


def list_posts(request):
    post_list = Post.objects.all()
    return render(request,
                  'malaria/list_posts.html',
                  {'post_list': post_list})


def view_post(request, post_id):

    retval = check(request)
    if retval is not None:
        return retval

    post = get_post_by_id(post_id)
    revpost = get_revpost_of_owner(post_id)
    # revpost may not exist yet so do not check it
    if post:
        return render(request,
                      'malaria/view_post.html',
                      {'post': post,
                       'revpost': revpost})
    else:
        raise Http404


def create_post(request):

    # check if the user is logged in
    retval = check(request)
    if retval is not None:
        return retval

    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user.pcuser
            post.save()
            return render(request,
                          'malaria/notice.html',
                          {'text': 'Post created successfully.',
                           'text1': 'Click here to view post.',
                           'post': post})
    return render(request,
                  'malaria/create_post.html',
                  {'form': form})


def edit_post(request, post_id):

    retval = check(request)
    if retval is not None:
        return retval

    post = get_post_by_id(post_id)
    if post:
        if request.method == 'POST':

            # need to get the original title_post and description_post
            # before it is changed when calling instance on PostForm
            orig_title = post.title_post
            orig_desc = post.description_post
            form = PostForm(request.POST, instance=post)

            if form.is_valid():

                owner = request.user.pcuser
                edited_title = form.cleaned_data['title_post']
                edited_desc = form.cleaned_data['description_post']

                if (orig_title != edited_title) or \
                   (orig_desc != edited_desc):

                    post = form.save(commit=False)
                    post.owner = owner
                    post.save()

                    revpost_title_change = False
                    revpost_desc_change = False

                    if(orig_title != edited_title):
                        revpost_title_change = True
                    if(orig_desc != edited_desc):
                        revpost_desc_change = True

                    revpost = RevPost(owner_rev=owner,
                                      owner_rev_post=post,
                                      title_post_rev=orig_title,
                                      description_post_rev=orig_desc,
                                      title_change=revpost_title_change,
                                      description_change=revpost_desc_change)
                    revpost.save()

                    return render(request,
                                  'malaria/notice.html',
                                  {'text': 'Post edited successfully.',
                                   'text1': 'Click here to view post.',
                                   'post': post})
                else:
                    return render(request,
                                  'malaria/notice.html',
                                  {'text': 'No changes to Post made.',
                                   'text1': 'Click here to view post.',
                                   'post': post})
            else:
                return render(request,
                              'malaria/edit_post.html',
                              {'form': form, 'post': post})
        else:
            form = PostForm(instance=post)
            return render(request,
                          'malaria/edit_post.html',
                          {'form': form, 'post': post})
    else:
        raise Http404


def delete_post(request, post_id):

    retval = check(request)
    if retval is not None:
        return retval

    if request.method == 'POST':
        if delete_post_by_id(post_id):
            return HttpResponseRedirect(reverse('malaria:list_posts'))
        else:
            raise Http404
    else:
        return render(request,
                      'malaria/delete_post.html',
                      {'post_id': post_id})


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Post endpoint that provides `list` and `detail` actions
    `list` action returns a list of all Posts
    `detail` action returns a particular Post instance based on id
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


@api_view(['GET', 'POST'])
def revpost_list(request):
    if request.method == 'GET':
        revpost = RevPost.objects.all()
        serializer = RevPostSerializer(revpost, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RevPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def revpost_detail(request, pk):
    try:
        revpost = RevPost.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # to do: the post below is undefined, fix it
        serializer = RevPostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RevPostSerializer(post, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        revpost.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RevPostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = RevPost.objects.all()
    serializer_class = RevPostSerializer
