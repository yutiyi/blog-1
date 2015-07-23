from wtforms import StringField

from .base import BaseForm


class ArticleForm(BaseForm):
    title = StringField('标题')
    body = StringField('内容')
