import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os.path
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        cookie = self.get_secure_cookie("count")
        count = int(cookie) + 1 if cookie else 1

        countString = "1 time" if count == 1 else "%d times" % count
        self.set_secure_cookie("count", str(count))

        self.write(
            '<html><head><title>Cookie Counter</title></head>'
            '<body><h1>You&rsquo;ve viewed this page %s times.</h1>'
            '</body></html>' % countString
        )


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
        ]
        settings = dict(
            # template_path=os.path.join(os.path.dirname(__file__), "templates"),
            # static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
            cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        )

        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
