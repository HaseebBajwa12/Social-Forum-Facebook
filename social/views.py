from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, QuerySet
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView, DeleteView

from posts.models import Notification
from rest_framework.response import Response

from .forms import CommentWForm, UpdatePostForm
from posts.models import Post, Comment, Image
from social.forms import PostForm, UpdateProfileForm, UpdateUserForm
from user_management.models import User, Profile
from django.http import Http404
from posts.models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, "landing/index.html")


class PostListView(View):
    def get(self, request, pk, *args, **kwargs):
        posts = Post.objects.filter().order_by("-created_at")
        print(posts)
        profile = User.objects.get(pk=pk)
        print(profile)
        form = PostForm()
        context = {
            "profile": profile,
            "post_list": posts,
            "form": form,

        }

        return render(request, "social/post_list.html", context)

    def post(self, request, *args, **kwargs):
        try:
            posts = Post.objects.all().order_by("-created_at")
            form = PostForm(request.POST, request.FILES)
            files = request.FILES
            profile = User.objects.get(pk=request.user.id)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.author = request.user
                new_post.save()
            context = {
                "profile": profile,
                "post_list": posts,
                "form": form,
            }

            return render(request, "social/post_list.html", context)
        except Exception as e:
            raise Http404("Something Went wrong")


class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            profile = User.objects.filter(pk=pk).first()
            user = profile
            posts = Post.objects.filter(author=user).order_by("-created_at")
            followers = profile.user_profile.followers.all()
            if len(followers) == 0:
                is_following = False
            for follower in followers:
                if follower == request.user:
                    is_following = True
                    break
                else:
                    is_following = False
            number_of_followers = len(followers)
            context = {
                "user": user,
                "profile": profile,
                "posts": posts,
                "number_of_followers": number_of_followers,
                "is_following": is_following,
            }

            return render(request, "social/user_profile.html", context)
        except Exception as e:
            raise Http404(f'Profile is not Exist against this {pk}')


class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):

        post = Post.objects.get(pk=pk)
        noti_obs = Notification.objects.filter().first()
        url = noti_obs.url
        description = noti_obs.description
        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if is_dislike:
            post.dislikes.remove(request.user)
        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        if not is_like:
            post.likes.add(request.user)

            Notification.objects.create(notification_type=1, from_user=request.user, to_user=post.author, post=post,
                                        description=description, url=url)
        if is_like:
            post.likes.remove(request.user)
        next = request.POST.get("next", "/")
        return HttpResponseRedirect(next)


class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        try:
            comment = Comment.objects.get(pk=pk)
            is_dislike = False
            for dislike in comment.dislikes.all():
                if dislike == request.user:
                    is_dislike = True
                    break
            if is_dislike:
                comment.dislikes.remove(request.user)
            is_like = False
            for like in comment.likes.all():
                if like == request.user:
                    is_like = True
                    break
            if not is_like:
                comment.likes.add(request.user)
                Notification.objects.create(
                    notification_type=1, from_user=request.user, to_user=comment.author, comment=comment
                )
            if is_like:
                comment.likes.remove(request.user)
            next = request.POST.get("next", "/")
            return HttpResponseRedirect(next)
        except Exception as e:
            raise Http404("Something Went Wrong")


class AddCommentDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):

        comment = Comment.objects.get(pk=pk)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)

        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get("next", "/")
        return HttpResponseRedirect(next)


class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        try:
            post = Post.objects.get(pk=pk)
            print(post.pk)
            form = CommentWForm()
            comments = Comment.objects.filter(post=post).order_by("-created_at")
            context = {
                "post": post,
                "form": form,
                "comments": comments,

            }
            return render(request, "social/post_detail.html", context)
        except Exception as e:
            raise Http404(f'Post detail is not exists against this {pk}')

    def post(self, request, pk, *args, **kwargs):
        try:
            post = Post.objects.get(pk=pk)
            form = CommentWForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.author = request.user
                new_comment.post = post
                new_comment.save()
                form.save()
                form = CommentWForm()
            comments = Comment.objects.filter(post=post).order_by("-created_at")
            Notification.objects.create(notification_type=2, from_user=request.user, to_user=post.author, post=post)
            context = {
                "post": post,
                "form": form,
                "comments": comments,
            }
            return render(request, "social/post_detail.html", context)
        except Exception as e:
            raise Http404("Something Went Wrong")


class PostEdit(View):
    def get(self, request, pk):

        post = Post.objects.get(pk=pk)
        print(post)
        form = UpdatePostForm(instance=post)
        print(form)
        return render(request, 'social/post_edit.html', {'form': form})

    def post(self, request, pk):
        try:
            instance = Post.objects.get(pk=pk)
            form = UpdatePostForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                form.save()
                url = reverse("post-detail", kwargs={'pk': pk})
                return HttpResponseRedirect(url)
        except Exception as e:
            raise Http404('something went wrong')


class UpdateProfileView(View):
    def get(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            form = UpdateProfileForm(instance=profile)
            user = User.objects.get(pk=pk)
            user_form = UpdateUserForm(instance=user)

            return render(request, 'social/update_profile.html', {'form': form, 'user_form': user_form, "pk": pk})
        except Exception as e:
            raise Http404(f'Profile is not Exists against this {pk}')

    def post(self, request, pk):
        try:
            print("before object")
            instance = Profile.objects.get(pk=pk)
            form = UpdateProfileForm(request.POST, request.FILES, instance=instance)
            user_instance = User.objects.get(pk=pk)
            user_form = UpdateUserForm(request.POST, instance=user_instance)
            if form.is_valid() and user_form.is_valid():
                form.save()
                user_form.save()
            print(form.errors, user_form.errors)
            url = reverse('post-list', kwargs={'pk': pk})
            return HttpResponseRedirect(url)
        except Exception as e:
            print(e)
            raise Http404("Something Went Wrong")


# class CommentEdit(View):
#     def get(self, request, pk):
#         comment_obj = Comment.objects.get(pk=pk)
#         form = CommentWForm(instance=comment_obj)
#         return render(request, 'social/edit_comment.html', {'form': form})
#
#     def post(self, request, pk):
#         instance = Comment.objects.get(pk=pk)
#         form = CommentWForm(request.POST, instance=instance)
#         if form.is_valid():
#             form.save()
#             url = reverse('post-detail', kwargs={'pk':pk})
#             return HttpResponseRedirect(url)


class PostCommentView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        try:
            post = Post.objects.get(pk=pk)
            form = CommentWForm()
            comments = Comment.objects.filter(post=post).order_by("-created_at")
            context = {
                "post": post,
                "form": form,
                "comments": comments,
            }
            return render(request, "social/post_list.html", context)
        except Exception as e:
            raise Http404(f"Comment is not exists against this {pk}")

    def post(self, request, pk, *args, **kwargs):
        try:

            post = Post.objects.get(pk=pk)
            form = CommentWForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.author = request.user
                new_comment.post = post
                new_comment.save()
                print(new_comment)

            comments = Comment.objects.filter(post=post).order_by("-created_at")
            Notification.objects.create(notification_type=2, from_user=request.user, to_user=post.author, post=post)
            context = {
                "post": post,
                "form": form,
                "comments": comments,
            }
            return render(request, "social/post_list.html", context)
        except Exception as e:
            raise Http404("Something Went Wrong")


class ListFollowers(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            profile = User.objects.get(pk=pk)

            followers = profile.user_profile.followers.all()
            context = {
                "profile": profile,
                "followers": followers,
            }
            return render(request, "social/followers_list.html", context)
        except Exception as e:
            raise Http404(f'Followers against this {pk} does not exists')


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['comment']
    template_name = "social/edit_comment.html"

    def get_success_url(self):
        pk = self.kwargs["post_pk"]
        print(pk)
        return reverse_lazy("post-detail", kwargs={"pk": pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentDeleteView(View):

    def get(self, request, pk, post_pk):
        try:
            comment_obj = Comment.objects.get(pk=pk)
            comment_obj.delete()
            url = reverse('post-detail', kwargs={"pk": post_pk})
            return HttpResponseRedirect(url)
        except Exception as e:
            raise Http404(f"comment not exists against this {pk}")


class PostNotification(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        try:
            notification = Notification.objects.get(pk=notification_pk)
            Post.objects.get(pk=post_pk)
            notification.user_has_seen = True
            notification.save()
            return redirect("post-list", pk=post_pk)
        except Exception as e:
            raise Http404("Something went wrong")


class CommentReplyView(LoginRequiredMixin, View):
    try:
        def post(self, request, post_pk, pk, *args, **kwargs):
            post = Post.objects.get(pk=post_pk)
            parent_comment = Comment.objects.get(pk=pk)
            form = CommentWForm(request.POST)

            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.author = request.user
                new_comment.post = post
                new_comment.parent = parent_comment
                new_comment.save()

            Notification.objects.create(
                notification_type=2, from_user=request.user, to_user=parent_comment.author, comment=new_comment
            )

            return redirect("post-detail", pk=post_pk)
    except Exception as e:
        raise Http404("Something Went Wrong")


# class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Post
#     template_name = "social/post_delete.html"
#     success_url = reverse_lazy("post-list")
#
#     def test_func(self):
#         post = self.get_object()
#         return self.request.user == post.author


class PostsDeleteView(View):
    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()
            url = reverse('post-list', kwargs={"pk": request.user.pk})
            return HttpResponseRedirect(url)
        except Exception as e:
            raise Http404(f"post not exist against this {pk}")


# class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Post
#     fields = ['description', 'image']
#     template_name = "social/post_edit.html"
#
#     def get_success_url(self):
#         pk = self.kwargs["pk"]
#         print(pk)
#         return reverse_lazy("post-detail", kwargs={"pk": pk})
#
#     def test_func(self):
#         post = self.get_object()
#         print(post)
#         return self.request.user == post.author


class RemoveNotification(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        try:

            notification = Notification.objects.get(pk=notification_pk)

            notification.user_has_seen = True
            notification.save()

            return HttpResponse("Success", content_type="text/plain")
        except Exception as e:
            raise Http404('something went wrong')


class FollowNotification(View):
    def get(self, request, notification_pk, profile_pk, *args, **kwargs):
        try:
            notification = Notification.objects.get(pk=notification_pk)
            User.objects.get(pk=profile_pk)

            notification.user_has_seen = True
            notification.save()

            return redirect("profile", pk=profile_pk)
        except Exception as e:
            raise Http404("something went wrong")


class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        try:
            profile = User.objects.get(pk=pk)
            profile.user_profile.followers.add(request.user)

            Notification.objects.create(notification_type=3, from_user=request.user, to_user=profile)

            return redirect("profile", pk=profile.pk)
        except Exception as e:
            raise Http404('something Went wrong')


class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        try:
            profile = User.objects.get(pk=pk)
            profile.user_profile.followers.remove(request.user)

            return redirect("profile", pk=profile.pk)
        except Exception as e:
            raise Http404('something Went wrong')


class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("query")
        print(query)
        profile_list = User.objects.filter(Q(username__icontains=query))
        context = {
            "profile_list": profile_list,
        }

        return render(request, "social/search.html", context)

# @login_required
# def NotifyHref(request, pk):
#     notify = get_object_or_404(Notification, pk=pk)
#     if notify.post:
#         return HttpResponseRedirect((reverse('post-list', args=[str(notify.post.pk)])))
#
#
# def CreateReactNotify(request, _type, post, words):
#     if request.user != post.author:
#         existed_notify = post.likes.count()
#         if int(existed_notify) >= 1:
#             for receiver in post.post_notify_people.all():
#                 Notification.objects.create(post=post, receiver=receiver, sender=request.user, notifications_type=_type,
#                                             text_preview="{0} and {1} {2} your post.".format(request.user.full_name(),
#                                                                                              existed_notify, words))
#         else:
#             for receiver in post.post_notify_people.all():
#                 Notification.objects.create(post=post, receiver=post.author, sender=request.user,
#                                             notifications_type=_type, notifications_obj=1,
#                                             text_preview="{0} {1} your post.".format(request.user.full_name(), words))
#
#     return print("done")
#
#
# def postValidation(user, post):
#     if post.page and user in post.page.page_blocked_members.all():
#         return True
#     elif post.group and user in post.group.group_members_blocked.all():
#         return True
#     elif user in post.author.blocked.all():
#         return True
#     elif post.author in user.blocked.all():
#         return True
#     else:
#         return False
#
#
# def LikePost(request, pk):
#     post = Post.objects.get(pk=pk)
#     if postValidation(request.user, post) == True:
#         return Response({'blocked': True})
#
#     elif request.user in post.likes.all():
#         post.likes.remove(request.user)
#         notify = Notification.objects.filter(post=post, receiver=post.author, sender=request.user,
#                                              notifications_type=1)
#         notify.delete()
#         post.save()
#         return Response(request, post)
#     else:
#
#         post.likes.add(request.user)
#         CreateReactNotify(request, 1, post, "liked")
#         return Response(request, post)
#
#
# def ActivatePostNotify(request, pk):
#     try:
#         post = Post.objects.get(pk=pk)
#         if request.user in post.post_notify_people.all():
#             post.post_notify_people.remove(request.user)
#         else:
#             post.post_notify_people.add(request.user)
#         return Response({"done": "done"})
#     except:
#         return Response({"error": "Whops something went wrong, or the object has been deleted."})
