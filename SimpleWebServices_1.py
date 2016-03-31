import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import options, define

define("port", default=8888, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')

def make_app():

    return tornado.web.Application([
        (r"/", IndexHandler)
    ])

if __name__ == "__main__":

    tornado.options.parse_command_line()

    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()

