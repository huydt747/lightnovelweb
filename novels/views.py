from django.shortcuts import render, get_object_or_404
from .models import Novel, Chapter

def novel_list(request):
    novels = Novel.objects.all()
    return render(request, '../templates/novels/novel_list.html', {'novels': novels})

def novel_detail(request, novel_id):
    novel = get_object_or_404(Novel, id=novel_id)
    chapters = novel.chapters.all()
    return render(request, '../templates/novels/novel_detail.html', {'novel': novel, 'chapters': chapters})

def chapter_detail(request, novel_id, chapter_number):
    chapter = get_object_or_404(Chapter, novel_id=novel_id, number=chapter_number)
    return render(request, '../templates/novels/chapter_detail.html', {'chapter': chapter})
