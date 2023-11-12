import datetime
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from rest_framework.authtoken.models import Token

from .models import AppUser, Post


token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc4MDgwMDQwLCJpYXQiOjE2Nzc5MDcyNDAsImp0aSI6IjZlNjg2MWEyYmYwMDQwZTdhYTQ2MDI0ZWJjYTEwMzE2IiwidXNlcl9pZCI6MX0.AEvEGwlGa0XznCv1j9Ra6xj9qebm9yXgQuaO5YBIQGk'


class AppUserTestCase(APITestCase):
    """
    Test suite for AppUsers
    """
    def setUp(self):
        self.client = APIClient()

        self.superuser = AppUser.objects.create(
            email='admin@admin.org',
            first_name='Admin',
            last_name='Main',
            member_id='U21',
            is_staff=True,
            is_active=True      
        )

        AppUser.objects.create(
            email='user@user.org',
            first_name='User',
            last_name='Main',
            member_id='U22',
            is_staff=False,
            is_active=False      
        )

        self.users = AppUser.objects.all()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_get_all_users(self):
        """
        test UserViewSet list method
        """ 
        self.assertEqual(self.users.count(), 2)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_one_user(self):
        """
        test UserViewSet retrieve method
        """
        for user in self.users:
            response = self.client.get(f'/api/users/{user.pk}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        data = {
            'email': 'new@new.org',
            'first_name': 'New First Name',
            'last_name': 'New Last Name',
            'member_id': 'UNEW',
            'is_staff': False,
        }

        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_user(self):
        data = {
            'id': self.superuser.pk,
            'email': 'aziz@admin.org',
            'first_name': 'Karim',
            'last_name': 'Main',
            'member_id': 'U21',
            'is_staff': True,
        }

        # updating user data
        response = self.client.put(f'/api/users/{self.superuser.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # checking if update was successfull
        get_resp = self.client.get(f'/api/users/{self.superuser.pk}/')
        self.assertEqual(get_resp.data['first_name'], 'Karim')

    def test_delete_user(self):
        response = self.client.delete(f'/api/users/{self.superuser.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PostTestCase(APITestCase):
    """
    Test suite for Posts
    """ 
    def setUp(self):
        self.client = APIClient()

        self.superuser = AppUser.objects.create(
            email='admin@admin.org',
            first_name='Admin',
            last_name='Main',
            member_id='U21',
            is_staff=True,
            is_active=True      
        )
    
        Post.objects.create(title='Title 1', body='Body 1', owner=self.superuser)
        Post.objects.create(title='Title 2', body='Body 2', owner=self.superuser)
        Post.objects.create(title='Title 3', body='Body 3', owner=self.superuser)
        Post.objects.create(title='Title 4', body='Body 4', owner=self.superuser)

        self.posts = Post.objects.all()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_get_all_posts(self):
        """
        test UserViewSet list method
        """ 
        self.assertEqual(self.posts.count(), 4)
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_post(self):
        """
        test UserViewSet retrieve method
        """
        for post in self.posts:
            response = self.client.get(f'/api/posts/{post.pk}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_one_user_all_posts(self):
        """
        test UserPostListView list method
        """
        response = self.client.get(f'/api/users/{self.superuser.pk}/posts')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_post(self):
        data = {
            'title': 'New Post Title',
            'body': 'New Post Body',
            'owner': self.superuser,
            'timestamp': datetime.datetime.now
        }

        response = self.client.post(f'/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_post(self):
        """
        test PostViewSet update method
        """ 
        data = {
            'id': self.posts.first().pk,
            'title': 'Updated',
            'body': 'Updated',
            'owner': self.posts.first().owner,
            'timestamp': self.posts.first().timestamp
        }

        # updating post data
        response = self.client.put(f'/api/posts/{self.posts.first().pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # checking if update was successfull
        get_resp = self.client.get(f'/api/posts/{self.posts.first().pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        """
        test PostViewSet delete method
        """ 
        response = self.client.delete(f'/api/posts/{self.posts.first().pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    

# class CommentTestCase(APITestCase):
#     """
#     Test suite for Comment
#     """ 
#     def setUp(self):
#         self.client = APIClient()

#         self.superuser = AppUser.objects.create(
#             email='admin@admin.org',
#             first_name='Admin',
#             last_name='Main',
#             member_id='U21',
#             is_staff=True,
#             is_active=True      
#         )
    
#         Post.objects.create(title='Title 1', body='Body 1', owner=self.superuser)
#         Post.objects.create(title='Title 2', body='Body 2', owner=self.superuser)

#         self.posts = Post.objects.all()

#         Comment.objects.create(content='Comment 1', post=self.posts.first(), owner=self.superuser)
#         Comment.objects.create(content='Comment 2', post=self.posts.first(), owner=self.superuser)

#         self.comments = Comment.objects.all()

#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    
#     def test_get_all_comments(self):
#         """
#         test action method in PostViewSet
#         """ 
#         self.assertEqual(self.comments.count(), 2)

#         for post in self.posts:
#             response = self.client.get(f'/api/posts/{post.pk}/comments/')
#             self.assertEqual(response.status_code, status.HTTP_200_OK)
    
#     def test_create_comment(self):
#         data = {
#             'content': 'COMMENT NEW 2',
#             'timestamp': datetime.datetime.now,
#             'post': self.posts.first(),
#             'owner': self.superuser
#         }

#         response = self.client.post(f'/api/posts/{self.posts.first().pk}/comment', data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_update_one_comment(self):
#         """
#         test CommenUpdateAPIView
#         """
#         data = {
#             'content': 'COMMENT 1 UPDATED',
#             'timestamp': self.comments.first().timestamp,
#             'post': self.comments.first().post,
#             'owner': self.comments.first().owner
#         }

#         response = self.client.put(f'/api/comments/{self.comments.first().pk}/update', data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
    
#     def test_delete_user(self):
#         """
#         test CommentDestroyView delete method
#         """ 
#         response = self.client.delete(f'/api/comments/{self.comments.first().pk}/delete')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)