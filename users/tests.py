from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

class LoginViewTest(TestCase):
    def setUp(self):
        # Tạo user test để login
        self.username = 'testuser'
        self.password = 'testpassword123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
    
    def test_login_page_loads(self):
        # Test GET request, trang login hiện form
        url = reverse('users:login')  # sửa lại theo tên url của bạn
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Đăng nhập")  # kiểm tra có chữ Đăng nhập trên trang

    def test_login_success(self):
        # Test POST với username, password đúng sẽ redirect thành công
        url = reverse('users:login')
        data = {
            'username': self.username,
            'password': self.password,
        }
        response = self.client.post(url, data)
        # Kiểm tra redirect về trang danh sách novel (novels:novel_list)
        self.assertRedirects(response, reverse('novels:novel_list'))
        # Kiểm tra user đã được login
        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.username, self.username)

    def test_login_fail_wrong_password(self):
        # POST với password sai thì form phải trả về lỗi, không redirect
        url = reverse('users:login')
        data = {
            'username': self.username,
            'password': 'wrongpassword',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        # Trang vẫn render login form (chưa redirect)
        self.assertContains(response, "Đăng nhập")
        # Kiểm tra user chưa được login
        user = response.wsgi_request.user
        self.assertFalse(user.is_authenticated)

    def test_login_fail_no_data(self):
        # POST với dữ liệu trống
        url = reverse('users:login')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Đăng nhập")
        user = response.wsgi_request.user
        self.assertFalse(user.is_authenticated)
