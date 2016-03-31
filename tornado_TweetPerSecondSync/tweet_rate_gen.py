import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.httpclient
import tornado.gen
from tornado.options import define, options
import urllib, urllib.parse
import json
import datetime
import time
import oauth2

CONSUMER_KEY = '9XKyjq769fZ883HfB8KbWT7AN'
CONSUMER_SECRET = 'sLXPcbkMEE90EfeaQMw7w89mg8O0yap5QXqryueQ7xw5pUG0St'
ACCESS_TOKEN = '393538660-CpHqO86niQJVBCdPgDYd7uKtF1ubDogIlSZ3DtQo'
ACCESS_TOKEN_SECRET = '3VfgebGM7IAdLqsz5Hm1hKD5pCN5KrJlocSco8lmBx0DP'


def authorize(url):
    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    token = oauth2.Token(key=ACCESS_TOKEN, secret=ACCESS_TOKEN_SECRET)

    params = {
        'oauth_version': '1.0',
        'oauth_nonce': oauth2.generate_nonce(),
        'oauth_timestamp': str(int(time.time())),
        'oauth_consumer_key': consumer.key,
        'oauth_token': token.key
        # 'oauth_signature_method':'HMAC-SHA1'
    }

    req = oauth2.Request(method="GET", url=url, parameters=params, is_form_encoded=True)

    req.sign_request(signature_method=oauth2.SignatureMethod_HMAC_SHA1(),
                     consumer=consumer,
                     token=token)
    return req.to_header()['Authorization'].encode(encoding='utf-8')


define("port", default=8888, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        query = self.get_argument('q')
        client = tornado.httpclient.AsyncHTTPClient()

        url = "https://api.twitter.com/1.1/search/tweets.json?" + \
              urllib.parse.urlencode(
                  {
                      "q": query,
                      "result_type": "recent",
                      "count": 100
                  }
              )
        response = yield tornado.gen.Task(client.fetch,
                                          request=url,
                                          headers={'Authorization': authorize(url=url)})

        if response.error:
            print("Error: ", response.error)
            print("[Bad] X-Rate-Limit-Remaining: ", response.headers['X-Rate-Limit-Remaining'])

        else:

            print("[Good] X-Rate-Limit-Remaining: ", response.headers['X-Rate-Limit-Remaining'])
            body = json.loads(response.body.decode("utf-8"))
            result_count = len(body['statuses'])
            now = datetime.datetime.now()
            raw_oldest_tweet_at = body['statuses'][-1]['created_at']
            oldest_tweet_at = datetime.datetime.strptime(raw_oldest_tweet_at,
                                                         "%a %b %d %H:%M:%S +0000 %Y")
            seconds_diff = time.mktime(now.timetuple()) - time.mktime(oldest_tweet_at.timetuple())
            tweets_per_second = float(result_count) / seconds_diff

            self.write("""
            <div style="text-align: center">
            <div style="font-size: 72px">%s</div>
            <div style="font-size: 144px">%.04f</div>
            <div style="font-size: 24px">tweets per second</div>
            </div>""" % (query, tweets_per_second))

            self.finish()


if __name__ == "__main__":
    tornado.options.parse_command_line()

    app = tornado.web.Application(handlers=[
        (r"/", IndexHandler)
    ], debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
