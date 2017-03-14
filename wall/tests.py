import datetime

from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client

from .models import *

class ApiTest(TestCase):


    def setUp(self):
        self.testuser = User.objects.create_user('admin', 'admin@test.com', 'pass')
        self.testuser.save()
        self.testuser.is_staff = True
        self.testuser.save()
        self.author = Authors.objects.create(user=self.testuser)
        self.author.save



    def test_create_user(self):
        user = User.objects.filter(email="admin@test.com")[0]
        self.assertTrue(user.email,True)

    def test_simple(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """

        self.assertIs(True, True)

    def test_create_message(self):
        self.testuser = User.objects.filter(username='admin')[0]
        m = Messages.objects.create(message="Test Message For Test",author=self.testuser.authors)
        m.save()
        saved_pk = m.pk
        m_from_db = Messages.objects.get(pk=m.pk)
        self.assertEqual(m.pk,m_from_db.pk)


    def test_create_comment_for_message(self):
        i = 10
        self.testuser = User.objects.filter(username='admin')[0]
        m = Messages.objects.create(message="Test Message For Test Comment", author=self.testuser.authors)
        for i in range (0,i):
            print(i)
            c = Comments.objects.create(message = m,comment_txt="COmmner",author=self.testuser.authors)
            c.save()
        total_count = Comments.objects.filter(message=m).count()
        self.assertEqual(total_count,i+1)



