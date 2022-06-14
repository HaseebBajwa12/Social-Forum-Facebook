from django import forms
from django.forms import ModelForm, ImageField

from posts.models import Comment, Post
from user_management.models import Profile, User


class PostForm(forms.ModelForm):
    description = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'rows': '3',
            'placeholder': 'Say Something...'
        }))

    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': True
        })
    )

    class Meta:
        model = Post
        fields = ['description', 'image']
        exclude = ('author', 'created_at', 'likes', 'dislikes', 'privacy')


class CommentWForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control', 'id': 'pw', 'style': 'width:400px; height:50px;',
                    'placeholder': 'Say Something...',
                }
            )
        }


class UpdateProfileForm(ModelForm):
    profile_image = ImageField(label='Profile_Image', widget=forms.FileInput)
    cover_image = ImageField(label='cover_Image', widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ['profile_image', 'cover_image', 'bio', 'gender']
        widgets = {
            'bio': forms.TextInput(
                attrs={'class': 'form-control', 'size': '3000', 'style': 'width:300px; '}),
            'gender': forms.TextInput(
                attrs={'class': 'form-control', 'size': '3000', 'style': 'width:300px; '}),
        }


class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'size': '3000', 'style': 'width:300px;'}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'size': '3000', 'style': 'width:300px;'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'size': '3000', 'style': 'width:300px;'}),

        }


class UpdatePostForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Post
        fields = ['description', 'image']
        exclude = ('author', 'created_at', 'likes', 'dislikes', 'privacy')

        widgets = {
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control', 'style': 'width:400px; height:150px;',

                }
            ),
            'image': forms.FileInput(),
        }
