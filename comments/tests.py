from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Comment
from novels.models import Novel
from .forms import CommentForm

User = get_user_model()

class CommentModelTest(TestCase):
    def setUp(self):
        # Tạo user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Tạo novel 
        self.novel = Novel.objects.create(
            title='Test Novel',
            author='Test Author',
            # Thêm các trường cần thiết khác dựa trên model Novel của bạn
        )
        
        # Tạo comment
        self.comment = Comment.objects.create(
            user=self.user,
            novel=self.novel,
            content='This is a test comment'
        )
        
        # Tạo reply comment
        self.reply = Comment.objects.create(
            user=self.user,
            novel=self.novel,
            content='This is a reply',
            parent=self.comment
        )
    
    def test_comment_creation(self):
        """Test comment được tạo đúng"""
        self.assertEqual(self.comment.content, 'This is a test comment')
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.novel, self.novel)
        self.assertIsNone(self.comment.parent)
    
    def test_comment_str_representation(self):
        """Test string representation của comment"""
        expected_str = f'{self.user.username} - {self.novel.title}'
        self.assertEqual(str(self.comment), expected_str)
    
    def test_reply_relationship(self):
        """Test mối quan hệ giữa comment và reply"""
        self.assertEqual(self.reply.parent, self.comment)
        self.assertEqual(self.comment.replies.first(), self.reply)
    
    def test_comment_deletion_cascade(self):
        """Test xóa comment sẽ xóa tất cả reply liên quan"""
        comment_id = self.comment.id
        reply_id = self.reply.id
        
        # Xóa comment chính
        self.comment.delete()
        
        # Kiểm tra cả comment và reply đều bị xóa
        self.assertFalse(Comment.objects.filter(id=comment_id).exists())
        self.assertFalse(Comment.objects.filter(id=reply_id).exists())
    
    def test_user_deletion_cascade(self):
        """Test xóa user sẽ xóa tất cả comment của user đó"""
        comment_id = self.comment.id
        
        # Xóa user
        self.user.delete()
        
        # Kiểm tra comment đã bị xóa
        self.assertFalse(Comment.objects.filter(id=comment_id).exists())
    
    def test_novel_deletion_cascade(self):
        """Test xóa novel sẽ xóa tất cả comment của novel đó"""
        comment_id = self.comment.id
        
        # Xóa novel
        self.novel.delete()
        
        # Kiểm tra comment đã bị xóa
        self.assertFalse(Comment.objects.filter(id=comment_id).exists())


class CommentFormTest(TestCase):
    def setUp(self):
        # Tạo user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Tạo novel
        self.novel = Novel.objects.create(
            title='Test Novel',
            author='Test Author',
            # Thêm các trường cần thiết khác dựa trên model Novel của bạn
        )
        
        # Tạo comment chính
        self.comment = Comment.objects.create(
            user=self.user,
            novel=self.novel,
            content='This is a test comment'
        )
    
    def test_comment_form_valid_data(self):
        """Test form với dữ liệu hợp lệ"""
        form = CommentForm(data={
            'content': 'This is a valid comment',
            'parent': ''
        })
        self.assertTrue(form.is_valid())
    
    def test_comment_form_valid_data_with_parent(self):
        """Test form với dữ liệu hợp lệ và có parent"""
        form = CommentForm(data={
            'content': 'This is a valid reply',
            'parent': self.comment.id
        })
        self.assertTrue(form.is_valid())
    
    def test_comment_form_blank_data(self):
        """Test form với dữ liệu trống"""
        form = CommentForm(data={
            'content': '',
            'parent': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
    
    def test_comment_form_render(self):
        """Test form rendering"""
        form = CommentForm()
        self.assertIn('rows="2"', str(form['content']))
        self.assertIn('class="w-full p-2 border rounded"', str(form['content']))
        self.assertIn('type="hidden"', str(form['parent']))


class CommentIntegrationTest(TestCase):
    def setUp(self):
        # Tạo user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Tạo novel
        self.novel = Novel.objects.create(
            title='Test Novel',
            author='Test Author',
            # Thêm các trường cần thiết khác dựa trên model Novel của bạn
        )
        
        # Tạo comment
        self.comment = Comment.objects.create(
            user=self.user,
            novel=self.novel,
            content='This is a test comment'
        )
    
    def test_save_comment_from_form(self):
        """Test lưu comment từ form"""
        form_data = {
            'content': 'New comment from form',
            'parent': ''
        }
        
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Lưu comment nhưng chưa commit
        new_comment = form.save(commit=False)
        new_comment.user = self.user
        new_comment.novel = self.novel
        new_comment.save()
        
        # Kiểm tra comment đã được lưu vào database
        saved_comment = Comment.objects.get(content='New comment from form')
        self.assertEqual(saved_comment.user, self.user)
        self.assertEqual(saved_comment.novel, self.novel)
    
    def test_save_reply_from_form(self):
        """Test lưu reply từ form"""
        form_data = {
            'content': 'This is a reply comment',
            'parent': self.comment.id
        }
        
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Lưu reply nhưng chưa commit
        new_reply = form.save(commit=False)
        new_reply.user = self.user
        new_reply.novel = self.novel
        new_reply.save()
        
        # Kiểm tra reply đã được lưu vào database
        saved_reply = Comment.objects.get(content='This is a reply comment')
        self.assertEqual(saved_reply.parent, self.comment)