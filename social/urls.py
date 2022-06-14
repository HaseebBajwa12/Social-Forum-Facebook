from django.urls import path

from .views import AddLike, AddCommentLike, CommentReplyView, PostsDeleteView, PostEdit, CommentUpdateView, \
    RemoveNotification, FollowNotification, AddFollower, RemoveFollower, UserSearch, AddCommentDislike
from .views import PostListView, UpdateProfileView, PostCommentView, ListFollowers, PostDetailView, CommentDeleteView, \
    PostNotification, ProfileView
from .views import Index

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("psts/<int:pk>/", PostListView.as_view(), name="post-list"),
    path("psts/<int:pk>/", PostCommentView.as_view(), name="post-comment"),
    path("psts/", PostListView.as_view(), name="post-list1"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path("post/<int:pk>/like", AddLike.as_view(), name="like"),
    path("post/<int:post_pk>/comment/<int:pk>/like", AddCommentLike.as_view(), name="comment-like"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(), name='update_profile'),
    path("profile/<int:pk>/followers/", ListFollowers.as_view(), name="list-followers"),
    path("post/<int:post_pk>/comment/<int:pk>/reply", CommentReplyView.as_view(), name="comment-reply"),
    path("post/<int:post_pk>/comment/delete/<int:pk>/", CommentDeleteView.as_view(), name="comment-delete"),
    path("post/delete/<int:pk>/", PostsDeleteView.as_view(), name="post-delete"),
    path("post/edit/<int:pk>/", PostEdit.as_view(), name="post-edit"),
    path("post/<int:post_pk>/comment/edit/<int:pk>/", CommentUpdateView.as_view(), name="comment-edit"),
    path("notification/delete/<int:notification_pk>", RemoveNotification.as_view(), name="notification-delete"),
    path("notification/<int:notification_pk>/post/<int:post_pk>", PostNotification.as_view(), name="post-notification"),
    path(
        "notification/<int:notification_pk>/profile/<int:profile_pk>",
        FollowNotification.as_view(),
        name="follow-notification",
    ),
    path("profile/<int:pk>/followers/add", AddFollower.as_view(), name="add-follower"),
    path("search/", UserSearch.as_view(), name="profile-search"),
    path("profile/<int:pk>/followers/remove", RemoveFollower.as_view(), name="remove-follower"),
    path("post/<int:post_pk>/comment/<int:pk>/dislike", AddCommentDislike.as_view(), name="comment-dislike"),

]
