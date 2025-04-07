import tornado.ioloop
import tornado.web
from customer_service.handle.agent_handle import ChatHandler

def make_app():
    return tornado.web.Application([
        (r"/api/chat", ChatHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running at http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()