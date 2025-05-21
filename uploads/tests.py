from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from novels.models import Novel, Chapter, Genre
from uploads.models import NovelUpload, ChapterUpload, GenreSelection

User = get_user_model()

class UploadViewsTest(TestCase):
    def setUp(self):
        # Tạo user và đăng nhập
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

        # Tạo genres dùng test form
        self.genre1 = Genre.objects.create(name='Fantasy')
        self.genre2 = Genre.objects.create(name='Adventure')

        # Tạo Novel và NovelUpload chuẩn bị test
        self.novel = Novel.objects.create(
            title="Existing Novel",
            description="Existing description",
            author="Existing Author",
            status="ongoing"
        )
        self.novel_upload = NovelUpload.objects.create(
            user=self.user,
            title="Test Upload",
            description="Test upload description",
            author="Test upload author",
            status="approved",
            novel=self.novel,
        )
        # Gắn genre cho novel qua GenreSelection
        GenreSelection.objects.create(novel_upload=self.novel_upload, genre=self.genre1)

        # Tạo chapter upload
        self.chapter_upload = ChapterUpload.objects.create(
            novel_upload=self.novel_upload,
            title="Chapter 1",
            content="Chapter 1 content",
            chapter_number=1
        )

    def test_upload_novel_get_and_post(self):
        url = reverse('upload_novel')
        # GET form
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

        # POST data valid để tạo novel upload
        post_data = {
            'title': 'New Novel',
            'description': 'New description',
            'author': 'New Author',
            'genres': [self.genre1.id, self.genre2.id],
        }
        with open('uploads/tests/test_cover.jpg', 'rb') as img:  # giả định có file test_cover.jpg
            response = self.client.post(url, {**post_data, 'cover_image': img})
        
        # Nếu không có ảnh test, bạn có thể bỏ cover_image hoặc dùng SimpleUploadedFile

        self.assertEqual(response.status_code, 302)  # redirect sang upload_chapter

        novel_upload = NovelUpload.objects.filter(title='New Novel', user=self.user).first()
        self.assertIsNotNone(novel_upload)
        self.assertEqual(novel_upload.genre_selections.count(), 2)

    def test_upload_chapter_get_and_post(self):
        url = reverse('upload_chapter', args=[self.novel_upload.id])

        # GET form
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

        # POST tạo chapter mới
        post_data = {
            'title': 'Chapter 2',
            'content': 'Content of chapter 2',
            'chapter_number': 2,
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('novels:novel_detail', args=[self.novel.id]))

        chapter = ChapterUpload.objects.filter(novel_upload=self.novel_upload, chapter_number=2).first()
        self.assertIsNotNone(chapter)
        self.assertEqual(chapter.title, 'Chapter 2')

    def test_my_uploads_view(self):
        url = reverse('my_uploads')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.novel_upload.title)

    def test_edit_novel_upload_get_and_post(self):
        url = reverse('edit_novel_upload', args=[self.novel_upload.id])
        
        # GET form with initial data
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

        # POST cập nhật data
        post_data = {
            'title': 'Updated Title',
            'description': 'Updated description',
            'author': 'Updated Author',
            'genres': [self.genre2.id],
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('my_uploads'))

        # Reload object and check update
        self.novel_upload.refresh_from_db()
        self.assertEqual(self.novel_upload.title, 'Updated Title')
        self.assertEqual(self.novel_upload.genre_selections.count(), 1)
        self.assertEqual(self.novel_upload.genre_selections.first().genre, self.genre2)

    def test_edit_chapter_get_and_post(self):
        url = reverse('edit_chapter', args=[self.chapter_upload.id])

        # GET form with initial data
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

        # POST cập nhật chapter
        post_data = {
            'title': 'Chapter 1 Updated',
            'content': 'Updated content',
            'chapter_number': 1,
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('upload_chapter', args=[self.novel_upload.id]))

        # Reload và kiểm tra cập nhật
        self.chapter_upload.refresh_from_db()
        self.assertEqual(self.chapter_upload.title, 'Chapter 1 Updated')
        self.assertEqual(self.chapter_upload.content, 'Updated content')
