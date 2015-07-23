import os.path

import tornado.web
from tornado.web import url
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from handlers.auth import LoginHandler, RegisterHandler, LogoutHandler
from handlers.home import HomeHandler

define('debug', default=True, type=bool)
define('port', default=8888, help='run on the given port', type=int)
define('init_db', default=False, type=bool)
define('database_url', type=str)
define('database_option_echo', type=bool)


class Application(tornado.web.Application):
    def __init__(self, db_session):
        handlers = [
            url(r'/login', LoginHandler, name='login'),
            url(r'/join', RegisterHandler, name='register'),
            url(r'/logout', LogoutHandler, name='logout'),
            url(r'/home', HomeHandler, name='home'),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            xsrf_cookies=True,
            cookie_secret='__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__',
            login_url='/login',
            autoescape=None,
        )
        settings.update(options.as_dict())
        self.db = db_session
        super(Application, self).__init__(handlers, **settings)

def init_db(engine):
    from models.base import Base
    Base.metadata.create_all(bind=engine)


def main():
    tornado.options.parse_command_line()
    if options.debug:
        tornado.options.parse_config_file(os.path.join(os.path.dirname(__file__), 'development.conf'))
    engine = create_engine(options.database_url, echo=options.database_option_echo)
    if options.init_db:
        init_db(engine)
    db_session = scoped_session(sessionmaker(bind=engine))
    http_server = tornado.httpserver.HTTPServer(Application(db_session))
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
