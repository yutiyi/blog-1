import tornado.web

from models.user import User


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    @property
    def get_current_user(self):
        # expires = self.get_secure_cookie('_expires')
        # if not expires or datetime.datetime.now() > expires:
        #     return None
        user_id = self.get_secure_cookie('_user_id')
        return None if user_id is None else self.db.query(User).filter(User.id == int(user_id)).first()

    def on_finish(self):
        self.db.remove()


class NewHandler(BaseHandler):
    model = None
    template_name = ''
    form_class = None
    success_url_name = ''

    def get(self):
        self.render(self.template_name, form=self.form_class())

    def post(self):
        form = self.form_class(self.request.body_arguments)
        if form.validate():
            obj = self.model()
            form.populate_obj(obj)
            self.db.add(obj)
            self.db.commit()
            return self.redirect(self.reverse_url(self.success_url_name))
        self.render(self.template_name, form=form)


class EditHandler(BaseHandler):
    model = None
    template_name = None
    form_class = None
    success_url_name = ''

    def obj(self, **kwargs):
        o = self.db.query(self.model).filter_by(**kwargs).first()
        if o is None:
            raise tornado.web.HTTPError(404)

    def get(self, **kwargs):
        obj = self.obj(**kwargs)
        self.render(self.template_name, form=self.form_class(obj=obj))

    def post(self, **kwargs):
        form = self.form_class(self.request.body_arguments)
        if form.validate():
            obj = self.obj(**kwargs)
            form.populate_obj(obj)
            self.db.add(obj)
            self.db.commit()
            return self.redirect(self.reverse_url(self.success_url_name))
        self.render(self.template_name, form=form)


class DeleteHandler(BaseHandler):
    model = None
    success_url_name = ''

    def get(self, **kwargs):
        o = self.db.query(self.model).filter_by(**kwargs).first()
        if o is None:
            raise tornado.web.HTTPError(404)
        self.db.remove(o)
        self.db.commit()
        self.redirect(self.reverse_url(self.success_url_name))
