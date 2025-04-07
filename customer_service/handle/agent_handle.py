import tornado.web
import json
from customer_service.agent.agent import RouteAgent

class ChatHandler(tornado.web.RequestHandler):
    async def post(self):
        try:
            data = json.loads(self.request.body.decode("utf-8"))
            message = data.get("message", "")
            if not message:
                self.write({"code": 1, "msg": "message 字段为空", "data": None})
                return

            router = RouteAgent()
            result = await  router.plan(message)
            self.write(result)

        except Exception as e:
            self.set_status(500)
            self.write({"code": 1, "msg": str(e), "data": None})