from django import forms

from blog.models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            "title",
            "description",
            "content",
            "slug",
            "published",
        ]


class ConfirmDeleteForm(forms.Form):
    """
    On crée un formulaire qui va représenter une case à cocher pour confirmer la suppression d'un article
    """
    confirm = forms.BooleanField(label="Je confirme la suppression")
