from time import sleep

from django.test import TestCase
import  datetime

from django.urls import reverse
from django.utils import timezone
from article.models import Article
from django.contrib.auth.models import User

# Create your tests here.

class ArticleModelTest(TestCase):

    def test_was_created_recently_with_future_article(self):
        #若文章创建时间为未来，返回False
        author = User(username='user', password='test_password')
        author.save()

        future_article = Article(
            author = author,
            title='test',
            content= 'test',
            created=timezone.now() + datetime.timedelta(days=30)
        )

        self.assertIs(future_article.was_created_recently(), False)



class ArticleViewTest(TestCase):

    def test_increase_views(self):
        #请求详情视图时，阅读量加一
        author = User(username='user2', password='password')
        author.save()
        article = Article(
            author =author,
            title='test4',
            content = 'test4',

        )
        article.save()
        self.assertIs(article.total_views, 0)

        url = reverse('article:article_detail', args=(article.id,))
        response = self.client.get(url)
        viewed_article = Article.objects.get(id = article.id)
        self.assertIs(viewed_article.total_views, 1)

    def test_increase_views_but_not_change_updated_field(self):
        author = User(username='test5', password='password')
        author.save()
        article = Article(
            author = author,
            title='test5',
            content='test5',
        )
        article.save()

        sleep(0.5)

        url = reverse('article:article_detail', args=(article.id,))
        response = self.client.get(url)

        viewed_article = Article.objects.get(id= article.id)
        self.assertIs(viewed_article.update - viewed_article.created < timezone.timedelta(seconds=0.1), True)