import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.auth
# import tornado.websocket
import os.path
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class TwitterHandler(tornado.web.RequestHandler, tornado.auth.TwitterMixin):
    @tornado.web.asynchronous
    def get(self):
        oAuthToken=self.get_secure_cookie('oauth_token')
        oAuthSecret=self.get_secure_cookie('oauth_secret')
        userID=self.get_secure_cookie('user_id')

        if self.get_argument('oauth_token', None):
            self.get_authenticated_user(self._twitter_on_auth)
            return

        elif oAuthToken and oAuthSecret:
            accessToken={
                'key':oAuthToken,
                'secret':oAuthSecret
            }
            self.twitter_request(
                '/users/show',
                access_token=accessToken,
                user_id=userID,
                callback=self._twitter_on_user
            )
            return
        self.authorize_redirect()

    def _twitter_on_auth(self, user):
        if not user:
            self.clear_all_cookies()
            raise tornado.web.HTTPError(500, 'Twitter authentication failed')

        self.get_secure_cookie('user_id', str(user['id']))
        self.get_secure_cookie('oauth_token', user['access_token']['key'])
        self.set_secure_cookie('oauth_secret', user['access_token']['secret'])

        self.redirect('/')

    def _twitter_on_user(self, user):
        if not user:
            self.clear_all_cookies()
            raise tornado.web.HTTPError(500, 'Couldn\'t retrieve user information')

        self.render('home.html', user=user)


class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_all_cookies()
        self.render('logout.html')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", TwitterHandler),
            (r"/logout", LogoutHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            #static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret="NTliOTY5NzJkYTVlMTU0OTAwMTdlNjgzMTA5M2U3OGQ5NDIxZmU3Mg==",
            #xsrf_cookies=True,
            #login_url="/login",
            twitter_consumer_key='9XKyjq769fZ883HfB8KbWT7AN',
            twitter_consumer_secret='sLXPcbkMEE90EfeaQMw7w89mg8O0yap5QXqryueQ7xw5pUG0St',
            debug=True,
        )

        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
