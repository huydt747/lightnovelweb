from django.shortcuts import render, get_object_or_404, redirect
from .models import Novel, Chapter
from comments.models import Comment
from comments.forms import CommentForm

def novel_list(request):
    novels = Novel.objects.all()
    return render(request, '../templates/novels/novel_list.html', {'novels': novels})

def novel_detail(request, novel_id):
    novel = get_object_or_404(Novel, pk=novel_id)
    comments = novel.comments.filter(parent__isnull=True).select_related('user').prefetch_related('replies')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.novel = novel
                comment.save()
                return redirect('novels:novel_detail', novel_id=novel.pk)
        else:
            return redirect('users:login')
    else:
        form = CommentForm()

    return render(request, 'novels/novel_detail.html', {
        'novel': novel,
        'comments': comments,
        'form': form
    })

def chapter_detail(request, novel_id, chapter_id):
    novel = get_object_or_404(Novel, id=novel_id)
    chapter = get_object_or_404(Chapter, id=chapter_id, novel=novel)
    return render(request, 'novels/chapter_detail.html', {'novel': novel, 'chapter': chapter})

