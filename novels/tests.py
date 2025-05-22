from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Genre, Novel, Chapter, SavedNovel

class GenreModelTest(TestCase):
    def test_genre_creation(self):
        """Kiểm tra nếu thể loại được tạo đúng cách"""
        genre = Genre.objects.create(name="Fantasy")
        self.assertEqual(str(genre), "Fantasy")

class NovelModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpass")
        self.genre = Genre.objects.create(name="Action")
        self.novel = Novel.objects.create(
            title="Test Novel",
            description="A test novel",
            author="Test Author",
            uploaded_by=self.user
        )
        self.novel.genres.add(self.genre)

    def test_novel_creation(self):
        """Kiểm tra nếu novel được tạo đúng cách"""
        self.assertEqual(self.novel.title, "Test Novel")
        self.assertEqual(self.novel.uploaded_by, self.user)
        self.assertIn(self.genre, self.novel.genres.all())

    def test_novel_string_representation(self):
        """Kiểm tra phương thức __str__ của Novel"""
        self.assertEqual(str(self.novel), "Test Novel")

class ChapterModelTest(TestCase):
    def setUp(self):
        self.novel = Novel.objects.create(title="Novel with Chapters", description="Test novel")
        self.chapter = Chapter.objects.create(
            novel=self.novel,
            title="Chapter 1",
            content="Content of chapter 1",
            chapter_number=1
        )

    def test_chapter_creation(self):
        """Kiểm tra nếu chapter được tạo đúng cách"""
        self.assertEqual(self.chapter.title, "Chapter 1")
        self.assertEqual(self.chapter.novel, self.novel)
        self.assertEqual(self.chapter.chapter_number, 1)

    def test_chapter_ordering(self):
        """Kiểm tra sắp xếp chapter theo chapter_number"""
        chapter2 = Chapter.objects.create(novel=self.novel, title="Chapter 2", content="...", chapter_number=2)
        chapters = Chapter.objects.filter(novel=self.novel)
        self.assertEqual(list(chapters), [self.chapter, chapter2])

    def test_chapter_string_representation(self):
        """Kiểm tra phương thức __str__ của Chapter"""
        self.assertEqual(str(self.chapter), "Novel with Chapters - Chapter 1")

class SavedNovelModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser2", password="testpass2")
        self.novel = Novel.objects.create(title="Saved Novel", description="Test novel")
        self.saved_novel = SavedNovel.objects.create(user=self.user, novel=self.novel)

    def test_saved_novel_creation(self):
        """Kiểm tra nếu saved novel được tạo đúng cách"""
        self.assertEqual(self.saved_novel.user, self.user)
        self.assertEqual(self.saved_novel.novel, self.novel)

    def test_saved_novel_unique_constraint(self):
        """Kiểm tra nếu một user không thể lưu cùng một novel hai lần"""
        duplicate_saved_novel = SavedNovel(user=self.user, novel=self.novel)
        with self.assertRaises(Exception):  # Django sẽ raise IntegrityError
            duplicate_saved_novel.save()

    def test_saved_novel_string_representation(self):
        """Kiểm tra phương thức __str__ của SavedNovel"""
        self.assertEqual(str(self.saved_novel), "testuser2 saved Saved Novel")