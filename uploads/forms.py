from django import forms
from .models import NovelUpload, ChapterUpload, GenreSelection
from novels.models import Genre

class NovelUploadForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = NovelUpload
        fields = ['title', 'description', 'author', 'cover_image', 'genres']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
    
    def save(self, commit=True, user=None):
        novel_upload = super().save(commit=False)
        if user:
            novel_upload.user = user
        
        if commit:
            novel_upload.save()
            
            genres = self.cleaned_data.get('genres', [])
            for genre in genres:
                GenreSelection.objects.create(
                    novel_upload=novel_upload,
                    genre=genre
                )
            
        return novel_upload

class ChapterUploadForm(forms.ModelForm):
    class Meta:
        model = ChapterUpload
        fields = ['title', 'content', 'chapter_number']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 15}),
        }