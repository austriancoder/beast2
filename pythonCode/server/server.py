import json
import os

from tornado import websocket, web, ioloop
import pigpio
from database import database as dbc

cl = []
componentstatus = []

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("../../web/index.html")


class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        if self not in cl:
            cl.append(self)
            print("Connection accepted from:" + repr(self.request.remote_ip))
            dbc.writeComponentsToJsonFile()
            self.write_message(decodejson())

    def on_message(self, message):
        print(message)
        dbc.setStatusForComponentInDB(message)
        dbc.writeComponentsToJsonFile()
        for client in cl:
            client.write_message(decodejson())
        #self.write_message(decodejson())
        #TX=25

        #BPS=2000

        #pi = pigpio.pi() # Connect to local Pi.
        #tx = vw.tx(pi, TX, BPS) # Specify Pi, tx gpio, and baud.,
        #msg = 0

        #start = time.time()

        #time.sleep(0.2)

        #tx.put([48, 49, 65, ((msg>>6)&0x3F)+32, (msg&0x3F)+32])

        #tx.put(message.format(msg))

    def on_close(self):
        if self in cl:
            cl.remove(self)


class ApiHandler(web.RequestHandler):
    @web.asynchronous
    def get(self, *args):
        self.finish()
        id = self.get_argument("id")
        value = self.get_argument("value")
        data = {"id": id, "value": value}
        data = json.dumps(data)
        for c in cl:
            c.write_message(data)

    @web.asynchronous
    def post(self):
        pass

settings = dict(
    static_path=os.path.join(os.path.dirname(__file__), "../../web/static"),
)

app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
    (r'/(favicon.ico)', web.StaticFileHandler, {'path': '../../web/static/images/'}),
], **settings)


def decodejson():
  #  json_data = json.loads()
 #   data = json.load(os.path.join(os.path.dirname(__file__), "../data/components.txt"), 'r')
   # json_data.close()
  #  for var in data:
 #       componentstatus.append(0)
  #  return data
    data=""
    with open ("../data/components.txt", "r") as myfile:
        data= myfile.read().replace('\n', '')
        data = data.replace(' ','')
    return data

if __name__ == '__main__':
    app.listen(8080)
    ioloop.IOLoop.instance().start()







