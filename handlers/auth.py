from .base import BaseHandler
from forms.auth import LoginForm, RegisterForm
from models.user import User


class LoginHandler(BaseHandler):
    def get(self):
        form = LoginForm()
        self.render('auth/login.html', form=form)

    def post(self):
        form = LoginForm(self.request.body_arguments)
        if form.validate():
            user = self.db.query(User).filter(User.email == form.email.data).first()
            if user is None:
                form.email.errors.append('用户名不存在')
                return self.render('auth/login.html', form=form)
            if not user.check_password(form.password.data):
                form.password.errors.append('密码错误')
                return self.render('auth/login.html', form=form)
            # self.set_secure_cookie('_expires', datetime.datetime.now())
            self.set_secure_cookie('_user_id', str(user.id))
            return self.redirect(self.reverse_url('home'))
        self.render('auth/login.html', form=form)


class RegisterHandler(BaseHandler):
    def get(self):
        form = RegisterForm()
        self.render('auth/register.html', form=form)

    def post(self):
        form = RegisterForm(self.request.body_arguments)
        if form.validate():
            user = self.db.query(User).filter(User.email == form.email.data).first()
            if user is not None:
                form.email.errors.append('邮箱已被使用')
                return self.render('auth/register.html', form=form)
            user = User(email=form.email.data, name=form.username.data)
            user.set_password(form.password.data)
            self.db.add(user)
            self.db.commit()
            self.redirect(self.reverse_url('login'))
        return self.render('auth/register.html', form=form)


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect(self.reverse_url('login'))
