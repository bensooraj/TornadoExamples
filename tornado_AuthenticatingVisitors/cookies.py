import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.websocket
from uuid import uuid4
import os.path
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")


class WelcomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("index.html",
                    user=self.current_user)


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        self.set_secure_cookie("username",
                               self.get_argument("username"))
        self.redirect("/")


class LogoutHandler(BaseHandler):
    def get(self):
        if (self.get_argument("logout", None)):
            self.clear_cookie("username")

        self.redirect("/")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", WelcomeHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            xsrf_cookies=True,
            login_url="/login",
            debug=True,
        )

        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
