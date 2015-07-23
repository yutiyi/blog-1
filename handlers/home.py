import tornado.web

from models.blog import Article
from forms.home import ArticleForm
from .base import BaseHandler, NewHandler, EditHandler, DeleteHandler


class HomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('home/index.html')


class ArticleNewHandler(NewHandler):
    model = Article
    template_name = 'home/article.html'
    form_class = ArticleForm
    success_url_name = 'home'


class ArticleEditHandler(EditHandler):
    model = Article
    template_name = 'home/article.html'
    form_class = ArticleForm
    success_url_name = 'home'


class ArticleDeleteHandler(DeleteHandler):
    model = Article
    success_url_name = 'home'
