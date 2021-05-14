from django import forms

from post.models import Post, Comment


class AddPostForm(forms.ModelForm):
    """
    Form for creating new post
    """
    picture = forms.ImageField(required=True)
    caption = forms.CharField(widget=forms.Textarea, required=True)
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter tags separated by #. (#tag1 #tag2)'}),
        required=True)

    class Meta:
        model = Post
        fields = ('picture', 'caption', 'tags')


class AddCommentForm(forms.ModelForm):
    """
    Form for creating comment
    """
    body = forms.CharField()

    class Meta:
        model = Comment
        fields = ('body',)
