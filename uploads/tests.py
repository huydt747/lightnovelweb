from django.test import TestCase
from django.contrib.auth import get_user_model
from novels.models import Novel, Genre
from .models import NovelUpload, ChapterUpload, GenreSelection
from django.core.exceptions import ValidationError
from .forms import NovelUploadForm, ChapterUploadForm

class NovelUploadTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.novel = Novel.objects.create(title="Test Novel")
        self.novel_upload = NovelUpload.objects.create(
            user=self.user,
            title="Uploaded Novel",
            description="A test novel description",
            author="Test Author",
            novel=self.novel,
            status="approved"
        )

    def test_novel_upload_creation(self):
        """Kiểm tra xem NovelUpload có được tạo đúng không"""
        self.assertEqual(self.novel_upload.title, "Uploaded Novel")
        self.assertEqual(self.novel_upload.user.username, "testuser")
        self.assertEqual(self.novel_upload.status, "approved")

    def test_get_genres_empty(self):
        """Kiểm tra trường hợp không có chapter nào"""
        self.assertEqual(self.novel_upload.get_genres().count(), 0)

class ChapterUploadTestCase(TestCase):
    def setUp(self):
        self.novel_upload = NovelUpload.objects.create(
            user=get_user_model().objects.create_user(username='testuser2', password='testpass2'),
            title="Another Novel",
            description="Description here",
            author="Author Name"
        )
        self.chapter = ChapterUpload.objects.create(
            novel_upload=self.novel_upload,
            title="Chapter 1",
            content="This is the first chapter",
            chapter_number=1
        )

    def test_chapter_creation(self):
        """Kiểm tra xem chapter có được lưu đúng không"""
        self.assertEqual(self.chapter.title, "Chapter 1")
        self.assertEqual(self.chapter.chapter_number, 1)

class GenreSelectionTestCase(TestCase):
    def setUp(self):
        self.novel_upload = NovelUpload.objects.create(
            user=get_user_model().objects.create_user(username='testuser3', password='testpass3'),
            title="Genre Test Novel",
            description="Some description",
            author="Author G"
        )
        self.genre = Genre.objects.create(name="Fantasy")
        self.genre_selection = GenreSelection.objects.create(
            novel_upload=self.novel_upload,
            genre=self.genre
        )

    def test_genre_selection_creation(self):
        """Kiểm tra xem thể loại có được liên kết đúng không"""
        self.assertEqual(self.genre_selection.genre.name, "Fantasy")
        self.assertEqual(self.genre_selection.novel_upload.title, "Genre Test Novel")

class NovelUploadAdvancedTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.novel = Novel.objects.create(title="Test Novel")
    
    def test_invalid_status_choice(self):
        """Kiểm tra nếu status có giá trị không hợp lệ"""
        novel_upload = NovelUpload(
            user=self.user,
            title="Invalid Status Novel",
            description="A test description",
            author="Author",
            status="invalid_choice"
        )
        with self.assertRaises(ValidationError):
            novel_upload.full_clean()

    def test_string_representation(self):
        """Kiểm tra hiển thị chuỗi của đối tượng NovelUpload"""
        novel_upload = NovelUpload.objects.create(
            user=self.user,
            title="Displayed Novel",
            description="A test novel",
            author="Test Author",
        )
        self.assertEqual(str(novel_upload), "Displayed Novel by testuser")

class ChapterUploadAdvancedTests(TestCase):
    def setUp(self):
        self.novel_upload = NovelUpload.objects.create(
            user=get_user_model().objects.create_user(username='testuser2', password='testpass2'),
            title="Novel with Chapters",
            description="Description here",
            author="Author Name"
        )

    def test_chapter_ordering(self):
        """Kiểm tra xem chương có sắp xếp đúng theo chapter_number"""
        chapter1 = ChapterUpload.objects.create(novel_upload=self.novel_upload, title="Ch1", content="...", chapter_number=1)
        chapter2 = ChapterUpload.objects.create(novel_upload=self.novel_upload, title="Ch2", content="...", chapter_number=2)

        chapters = ChapterUpload.objects.filter(novel_upload=self.novel_upload)
        self.assertEqual(list(chapters), [chapter1, chapter2])

    def test_chapter_string_representation(self):
        """Kiểm tra hiển thị chuỗi của đối tượng ChapterUpload"""
        chapter = ChapterUpload.objects.create(novel_upload=self.novel_upload, title="Chapter Test", content="...", chapter_number=5)
        self.assertEqual(str(chapter), "Novel with Chapters - Chapter 5")

class GenreSelectionAdvancedTests(TestCase):
    def setUp(self):
        self.novel_upload = NovelUpload.objects.create(
            user=get_user_model().objects.create_user(username='testuser3', password='testpass3'),
            title="Genre Test Novel",
            description="Some description",
            author="Author G"
        )
        self.genre1 = Genre.objects.create(name="Fantasy")
        self.genre2 = Genre.objects.create(name="Adventure")

    def test_genre_uniqueness(self):
        """Kiểm tra nếu cùng một thể loại bị thêm hai lần vào cùng một novel_upload"""
        GenreSelection.objects.create(novel_upload=self.novel_upload, genre=self.genre1)
        duplicate_genre = GenreSelection(novel_upload=self.novel_upload, genre=self.genre1)

        with self.assertRaises(ValidationError):
            duplicate_genre.full_clean()

    def test_genre_string_representation(self):
        """Kiểm tra hiển thị chuỗi của đối tượng GenreSelection"""
        genre_selection = GenreSelection.objects.create(novel_upload=self.novel_upload, genre=self.genre2)
        self.assertEqual(str(genre_selection), "Genre Test Novel - Adventure")

class NovelUploadFormTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.genre1 = Genre.objects.create(name="Fantasy")
        self.genre2 = Genre.objects.create(name="Adventure")
    
    def test_valid_form_submission(self):
        """Kiểm tra nếu form hợp lệ và lưu novel + genres đúng cách"""
        form_data = {
            'title': 'Test Novel',
            'description': 'This is a test novel',
            'author': 'Test Author',
            'genres': [self.genre1.id, self.genre2.id]
        }
        form = NovelUploadForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        novel_upload = form.save(commit=True, user=self.user)

        self.assertEqual(novel_upload.title, "Test Novel")
        self.assertEqual(novel_upload.user, self.user)
        self.assertEqual(novel_upload.genre_selections.count(), 2)

    def test_invalid_form_missing_title(self):
        """Kiểm tra nếu thiếu title thì form không hợp lệ"""
        form_data = {
            'description': 'No title',
            'author': 'Anonymous'
        }
        form = NovelUploadForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

### Test cho `ChapterUploadForm`
class ChapterUploadFormTestCase(TestCase):
    def setUp(self):
        self.novel_upload = NovelUpload.objects.create(
            user=get_user_model().objects.create_user(username='testuser2', password='testpass2'),
            title="Novel with Chapters",
            description="Description here",
            author="Author Name"
        )

    def test_valid_chapter_creation(self):
        """Kiểm tra nếu form hợp lệ và tạo chương đúng cách"""
        form_data = {
            'title': 'Chapter 1',
            'content': 'This is the first chapter',
            'chapter_number': 1
        }
        form = ChapterUploadForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        chapter = form.save(commit=False)
        chapter.novel_upload = self.novel_upload
        chapter.save()

        self.assertEqual(chapter.title, "Chapter 1")
        self.assertEqual(chapter.novel_upload, self.novel_upload)
        self.assertEqual(chapter.chapter_number, 1)

    def test_invalid_chapter_missing_content(self):
        """Kiểm tra nếu thiếu nội dung thì form không hợp lệ"""
        form_data = {
            'title': 'Chapter with no content',
            'chapter_number': 2
        }
        form = ChapterUploadForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)