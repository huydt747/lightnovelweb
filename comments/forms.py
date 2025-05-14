from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'parent']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'class': 'w-full p-2 border rounded'}),
            'parent': forms.HiddenInput()
        }
