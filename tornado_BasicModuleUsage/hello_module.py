import os.path
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import define, options

define("port", default=8888, type=int, help="Run on the given port")


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('hello.html')


class HelloModule(tornado.web.UIModule):
    def render(self):
        return '<h1>Hello, world!</h1>'


def make_app():
    return tornado.web.Application(

        handlers=[
            (r'/', HelloHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        ui_modules={'Hello': HelloModule},
        debug=True)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = make_app()

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(port=options.port)

    tornado.ioloop.IOLoop.instance().start()
