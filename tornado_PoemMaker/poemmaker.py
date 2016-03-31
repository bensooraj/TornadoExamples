import os.path
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import define, options

define('port', default=8888, type=int, help="Run on the given port")


class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')


class PoemPageHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        verb = self.get_argument('verb')
        noun3 = self.get_argument('noun3')

        self.render('poem.html', roads=noun1, wood=noun2, made=verb, difference=noun3)


def make_app():
    return tornado.web.Application([
        (r"/", IndexHandler),
        (r"/poem", PoemPageHandler)
    ], template_path=os.path.join(os.path.dirname(__file__), "templates")
    )


if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()
