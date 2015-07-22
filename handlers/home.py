import tornado.web
from .base import BaseHandler, NewHandler, EditHandler, DeleteHandler


class HomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('home/index.html')


class ArticleNewHandler(NewHandler):
    pass


class ArticleEditHandler(EditHandler):
    pass


class ArticleDeleteHandler(DeleteHandler):
    pass
