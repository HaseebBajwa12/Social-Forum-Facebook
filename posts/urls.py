from django.urls import path
from .views import (
    UserSearch,
    # seen_test,
     test,
)

urlpatterns = [
    path("search/", UserSearch.as_view(), name="profile-search"),
    # path('home/', seen_test, name="home"),
    path('test/', test, name="home"),


]

