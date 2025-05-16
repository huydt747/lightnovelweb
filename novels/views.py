from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Novel, Chapter
from comments.models import Comment
from comments.forms import CommentForm

def novel_list(request):
    novels = Novel.objects.all()
    return render(request, '../templates/novels/novel_list.html', {'novels': novels})

def novel_detail(request, novel_id):
    novel = get_object_or_404(Novel, pk=novel_id)
    comments = novel.comments.filter(parent__isnull=True).select_related('user').prefetch_related('replies')

    # Lấy danh sách ID truyện đã lưu (nếu người dùng đã đăng nhập)
    saved_novel_ids = []
    if request.user.is_authenticated:
        saved_novel_ids = list(request.user.saved_novels.values_list('novel_id', flat=True))

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
        'form': form,
        'saved_novel_ids': saved_novel_ids,
    })

def chapter_detail(request, novel_id, chapter_id):
    novel = get_object_or_404(Novel, id=novel_id)
    chapter = get_object_or_404(Chapter, id=chapter_id, novel=novel)

    prev_chapter = Chapter.objects.filter(
        novel=novel, chapter_number__lt=chapter.chapter_number
    ).order_by('-chapter_number').first()

    next_chapter = Chapter.objects.filter(
        novel=novel, chapter_number__gt=chapter.chapter_number
    ).order_by('chapter_number').first()

    return render(request, 'novels/chapter_detail.html', {
        'novel': novel,
        'chapter': chapter,
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,
    })


