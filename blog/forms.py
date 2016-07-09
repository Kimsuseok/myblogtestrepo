from django import forms
from .models import Post, Uploadfile

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', )  #'__all__'


class ImageForm(forms.ModelForm):

    class Meta:
        model = Uploadfile
        fields = ('file', )