import tornado.web
from models.user import User


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        # expires = self.get_secure_cookie('_expires')
        # if not expires or datetime.datetime.now() > expires:
        #     return None
        user_id = self.get_secure_cookie('_user_id')
        if not user_id:
            return None
        return self.db.query(User).filter(User.id == int(user_id)).first()

    def on_finish(self):
        self.db.remove()


class NewHandler(BaseHandler):
    pass


class EditHandler(BaseHandler):
    pass


class DeleteHandler(BaseHandler):
    pass
