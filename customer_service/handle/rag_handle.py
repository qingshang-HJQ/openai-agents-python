import json
import os
import traceback

import tornado.web

from customer_service.RAG.file_parser import parse_file_and_embed
from customer_service.RAG.service import upload_file




class ChatHandler(tornado.web.RequestHandler):
    def post(self):
        res = {"code": 1, "msg": "上传成功", "data": None}
        try:
            upload = self.request.files.get("file", None)
            body = self.request.body
            try:
                if not json.loads(body):
                   raise "json parse error"
            except Exception as e:
                print(traceback.format_exc())
            if not upload:
                res["msg"] = "未上传文件"
            else:
                fileinfo = upload[0]
                filename = fileinfo.filename
                if not filename.endswith((".pdf", ".doc", ".docx",".txt")):
                    res["msg"] = "文件格式错误"
                res["data"] = upload_file(fileinfo,body)
        except:
            print(traceback.format_exc())
            self.set_status(500)
        self.write(tornado.escape.json_encode(res))