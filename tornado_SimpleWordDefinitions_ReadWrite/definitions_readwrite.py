import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo
from pymongo import MongoClient
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class WordHandler(tornado.web.RequestHandler):
    def get(self, word):
        coll = self.application.db.words
        word_doc = coll.find_one({"word": word})
        if word_doc:
            del word_doc["_id"]
            self.write(word_doc)
        else:
            self.set_status(404)
            error_msg = "Oops! Looks like " + word + " doesn't exist in our database"
            self.write({"error": error_msg})


    def post(self, word):
        definition = self.get_argument("definition")
        coll = self.application.db.words
        word_doc = coll.find_one({"word":word})
        if word_doc:
            word_doc["definition"] = definition
            coll.save(word_doc)
        else:
            word_doc = {'word': word, 'definition': definition}
            coll.insert(word_doc)

        del word_doc["_id"]
        self.write(word_doc)



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/(\w+)", WordHandler)
        ]
        settings = dict(
            #     template_path=os.path.join(os.path.dirname(__file__), "templates"),
            #     static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True
        )
        client = MongoClient('mongodb://localhost:27017/')
        self.db = client["example"]

        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port=options.port)
    tornado.ioloop.IOLoop.instance().start()
