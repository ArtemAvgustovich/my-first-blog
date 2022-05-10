from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Post

"""
create a user
user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

from django.contrib.auth import authenticate
user = authenticate(username='john', password='secret')
if user is not None:
    # A backend authenticated the credentials
else:
    # No backend authenticated the credentials 
"""

def create_post(author, created_date, published_date=timezone.now(), text='', title=''):
   return Post.objects.create(
       author=author,
       created_date=created_date,
       published_date=published_date,
       text=text,
       title=title,
   )


class PostListViewTests(TestCase):

    def test_no_posts(self):
        """
        If no posts exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts here yet...")
        self.assertQuerysetEqual(response.context['posts'], [])
    


