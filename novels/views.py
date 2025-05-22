from django.shortcuts import render, get_object_or_404, redirect
from .models import Novel, Chapter, Genre
from comments.forms import CommentForm

def homepage(request):
    try:
        supernatural_genre = Genre.objects.get(id=4)
        supernatural_novels = Novel.objects.filter(genres=supernatural_genre).distinct()
    except Genre.DoesNotExist:
        supernatural_genre = None
        supernatural_novels = []

    return render(request, '../templates/novels/novel_list.html', {
        'supernatural_novels': supernatural_novels,
        'genre': supernatural_genre,
    })


def novel_list(request):
    all_novels = Novel.objects.all()  # hoặc truyện mới cập nhật

    # Lấy thể loại Siêu nhiên (id=4)
    try:
        genre_supernatural = Genre.objects.get(id=4)
        supernatural_novels = Novel.objects.filter(genres=genre_supernatural).distinct()
    except Genre.DoesNotExist:
        genre_supernatural = None
        supernatural_novels = []

    # Lấy thể loại Hành động (id=2)
    try:
        genre_action = Genre.objects.get(id=2)
        action_novels = Novel.objects.filter(genres=genre_action).distinct()
    except Genre.DoesNotExist:
        genre_action = None
        action_novels = []

    # Lấy thể loại id=1 (ví dụ tên gì đó)
    try:
        genre_one = Genre.objects.get(id=1)
        one_novels = Novel.objects.filter(genres=genre_one).distinct()
    except Genre.DoesNotExist:
        genre_one = None
        one_novels = []

    return render(request, 'novels/novel_list.html', {
        'novels': all_novels,
        'genre_supernatural': genre_supernatural,
        'supernatural_novels': supernatural_novels,
        'genre_action': genre_action,
        'action_novels': action_novels,
        'genre_one': genre_one,
        'one_novels': one_novels,
    })



def novel_detail(request, novel_id):
    novel = get_object_or_404(Novel, pk=novel_id)
    comments = novel.comments.filter(parent__isnull=True).select_related('user').prefetch_related('replies')

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

def genre_filter(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    novels = Novel.objects.filter(genres=genre)
    return render(request, 'novels/genre_filter.html', {
        'genre': genre,
        'novels': novels
    })
    
def original_novels(request):
    tu_sang_tac = get_object_or_404(Genre, name="Tự sáng tác")
    novels = Novel.objects.filter(genres=tu_sang_tac)
    return render(request, 'novels/original.html', {
        'novels': novels,
        'genre': tu_sang_tac
    })
    
def search_novels(request):
    query = request.GET.get('q', '')
    novels = Novel.objects.filter(title__icontains=query) if len(query) >= 2 else []

    return render(request, 'novels/search_results.html', {
        'query': query,
        'novels': novels
    })
