from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseForbidden

from .forms import NovelUploadForm, ChapterUploadForm
from .models import NovelUpload, ChapterUpload
from novels.models import Novel, Chapter, Genre

@login_required
def upload_novel(request):
    if request.method == 'POST':
        form = NovelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Lưu upload
            novel_upload = form.save(user=request.user)
            
            # Tạo novel từ upload
            novel = Novel.objects.create(
                title=novel_upload.title,
                description=novel_upload.description,
                author=novel_upload.author,
                cover_image=novel_upload.cover_image,
                status='ongoing'
            )
            
            # Liên kết novel với upload
            novel_upload.novel = novel
            novel_upload.save()
            
            # Thêm thể loại cho novel
            genres = form.cleaned_data.get('genres', [])
            for genre in genres:
                novel.genres.add(genre)
            
            messages.success(request, 'Truyện đã được tạo thành công!')
            return redirect('upload_chapter', novel_upload_id=novel_upload.id)
    else:
        form = NovelUploadForm()
    
    return render(request, 'uploads/upload_novel.html', {'form': form})

@login_required
def upload_chapter(request, novel_upload_id):
    novel_upload = get_object_or_404(NovelUpload, id=novel_upload_id)
    
    # Kiểm tra quyền truy cập
    if novel_upload.user != request.user:
        return HttpResponseForbidden("Bạn không có quyền thêm chương cho truyện này.")
    
    if request.method == 'POST':
        form = ChapterUploadForm(request.POST)
        if form.is_valid():
            chapter_upload = form.save(commit=False)
            chapter_upload.novel_upload = novel_upload
            chapter_upload.save()
            
            # Tạo chapter trong novels app
            if novel_upload.novel:
                Chapter.objects.create(
                    novel=novel_upload.novel,
                    title=chapter_upload.title,
                    content=chapter_upload.content,
                    chapter_number=chapter_upload.chapter_number
                )
            
            messages.success(request, 'Chương mới đã được tạo thành công!')
            
            # Xác định hành động tiếp theo
            if 'save_and_add' in request.POST:
                return redirect('upload_chapter', novel_upload_id=novel_upload.id)
            else:
                return redirect('novels:novel_detail', novel_id=novel_upload.novel.id)
    else:
        # Tự động điền số chương tiếp theo
        next_chapter = novel_upload.chapters.count() + 1
        form = ChapterUploadForm(initial={'chapter_number': next_chapter})
    
    chapters = ChapterUpload.objects.filter(novel_upload=novel_upload).order_by('chapter_number')
    
    return render(request, 'uploads/upload_chapter.html', {
        'form': form,
        'novel_upload': novel_upload,
        'chapters': chapters
    })

@login_required
def my_uploads(request):
    uploads = NovelUpload.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'uploads/my_uploads.html', {'uploads': uploads})

@login_required
def edit_novel_upload(request, novel_upload_id):
    novel_upload = get_object_or_404(NovelUpload, id=novel_upload_id)
    
    # Kiểm tra quyền truy cập
    if novel_upload.user != request.user:
        return HttpResponseForbidden("Bạn không có quyền chỉnh sửa truyện này.")
    
    if request.method == 'POST':
        form = NovelUploadForm(request.POST, request.FILES, instance=novel_upload)
        if form.is_valid():
            novel_upload = form.save()
            
            # Cập nhật novel liên kết
            if novel_upload.novel:
                novel = novel_upload.novel
                novel.title = novel_upload.title
                novel.description = novel_upload.description
                novel.author = novel_upload.author
                if novel_upload.cover_image:
                    novel.cover_image = novel_upload.cover_image
                novel.save()
                
                # Cập nhật thể loại
                novel.genres.clear()
                genres = form.cleaned_data.get('genres', [])
                for genre in genres:
                    novel.genres.add(genre)
            
            messages.success(request, 'Thông tin truyện đã được cập nhật!')
            return redirect('my_uploads')
    else:
        # Lấy thể loại hiện tại
        initial_genres = []
        if novel_upload.novel:
            initial_genres = novel_upload.novel.genres.all()
        
        form = NovelUploadForm(instance=novel_upload, initial={'genres': initial_genres})
    
    return render(request, 'uploads/edit_novel.html', {'form': form, 'novel_upload': novel_upload})

@login_required
def edit_chapter(request, chapter_id):
    chapter_upload = get_object_or_404(ChapterUpload, id=chapter_id)
    novel_upload = chapter_upload.novel_upload
    
    # Kiểm tra quyền truy cập
    if novel_upload.user != request.user:
        return HttpResponseForbidden("Bạn không có quyền chỉnh sửa chương này.")
    
    if request.method == 'POST':
        form = ChapterUploadForm(request.POST, instance=chapter_upload)
        if form.is_valid():
            chapter_upload = form.save()
            
            # Cập nhật chapter trong novels app
            if novel_upload.novel:
                try:
                    chapter = Chapter.objects.get(
                        novel=novel_upload.novel,
                        chapter_number=chapter_upload.chapter_number
                    )
                    chapter.title = chapter_upload.title
                    chapter.content = chapter_upload.content
                    chapter.save()
                except Chapter.DoesNotExist:
                    # Tạo chapter mới nếu không tìm thấy
                    Chapter.objects.create(
                        novel=novel_upload.novel,
                        title=chapter_upload.title,
                        content=chapter_upload.content,
                        chapter_number=chapter_upload.chapter_number
                    )
            
            messages.success(request, 'Chương đã được cập nhật!')
            return redirect('upload_chapter', novel_upload_id=novel_upload.id)
    else:
        form = ChapterUploadForm(instance=chapter_upload)
    
    return render(request, 'uploads/edit_chapter.html', {
        'form': form,
        'chapter': chapter_upload,
        'novel_upload': novel_upload
    })