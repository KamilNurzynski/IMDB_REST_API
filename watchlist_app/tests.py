from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from watchlist_app.api import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review
from rest_framework.test import force_authenticate


class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='example', password='Gladorota2')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)  # ze strony django rest-framework
        self.stream_platform = StreamPlatform.objects.create(name='Fiutflix', about='Bardzo galante filmy',
                                                             website="http://netflix.com")

    def test_streamplatform_create_user_without_permission(self):
        data = {
            'name': 'Fiutflix',
            'about': 'Bardzo galante filmy',
            'website': "http://netflix.com"
        }
        response = self.client.post(reverse('stream_platform_list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_get_list_user_without_permission(self):
        response = self.client.get(reverse('stream_platform_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_details(self):
        # zwróć uwagę na konstrukcję reverse poniżej
        response = self.client.get(reverse('stream_platform_details', args=(self.stream_platform.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_details_put(self):
        response = self.client.put(reverse('stream_platform_details', args=(self.stream_platform.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_details_delete(self):
        response = self.client.delete(reverse('stream_platform_details', args=(self.stream_platform.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class WatchListTestCase(APITestCase):
    # dotyczy WatchListAV
    def setUp(self):
        self.user = User.objects.create_user(username='example', password='Gladorota2')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)  # ze strony django rest-framework
        self.stream_platform = StreamPlatform.objects.create(name='Fiutflix', about='Bardzo galante filmy',
                                                             website="http://netflix.com")
        self.watch = WatchList.objects.create(title='Nossolar', storyline='about sth',
                                              stream_platform=self.stream_platform, active=True)

    def test_watchlist_create(self):
        data = {
            'title': 'Nossolar',
            'storyline': 'about sth',
            'stream_platform': self.stream_platform,
            'active': True
        }
        response = self.client.post(reverse('movie_list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_get_list(self):
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_details_get(self):
        response = self.client.get(reverse('movie_details', args=(self.watch.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(WatchList.objects.get(pk=1).title, 'Nossolar')
        self.assertEqual(WatchList.objects.get(pk=1).stream_platform, self.stream_platform)
        self.assertEqual(WatchList.objects.count(), 1)


class ReviewCreateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='example', password='Gladorota2')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)  # ze strony django rest-framework
        self.stream_platform = StreamPlatform.objects.create(name='Fiutflix', about='Bardzo galante filmy',
                                                             website="http://netflix.com")
        self.watch = WatchList.objects.create(title='Nossolar', storyline='about sth',
                                              stream_platform=self.stream_platform, active=True)
        #
        self.watch2 = WatchList.objects.create(title='Nossolar', storyline='about sth',
                                               stream_platform=self.stream_platform, active=True)
        self.review = Review.objects.create(author=self.user, rating=5, description='great', watchlist=self.watch2,
                                            active=True)

    def test_review_create(self):
        data = {
            'author': self.user,
            'rating': 5,
            'description': 'sth',
            'watchlist': self.watch,
            'active': True
        }

        response = self.client.post(reverse('review_create', args=(self.watch.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.get(pk=1).rating, 5)
        self.assertEqual(Review.objects.count(), 2)
        # poniżej proba ponownego utworzenia i bad request
        response = self.client.post(reverse('review_create', args=(self.watch.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauthenticated(self):
        data = {
            'author': self.user,
            'rating': 5,
            'description': 'sth',
            'watchlist': self.watch,
            'active': True
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review_create', args=(self.watch.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            'author': self.user,
            'rating': 5,
            'description': 'sth-updated',
            'watchlist': self.watch,
            'active': False
        }
        response = self.client.put(reverse('review_details', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reviews_of_movie_get_list(self):
        response = self.client.get(reverse('review_list', args=(self.watch.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_of_movie_get_method(self):
        response = self.client.get(reverse('review_list', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_details_delete(self):
        response = self.client.delete(reverse('review_details', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_review_user(self):
        response = self.client.get('/api/watch/user_reviews/?username=' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
