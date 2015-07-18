import tornado.web
from .base import BaseHandler


class HomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('home/index.html')


class EntryHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('home/index.html')
