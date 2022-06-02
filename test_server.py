import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
import numpy as np
from PIL import Image
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
import imp

class Resquest(BaseHTTPRequestHandler):
    def handler(self):
        print("data:", self.rfile.readline().decode())
        self.wfile.write(self.rfile.readline())

    def do_GET(self):
        print(self.requestline)
        if self.path != '/hello':
            self.send_error(404, "Page not Found!")
            return
        data = {
            'result_code': '1',
            'result_desc': 'Success',
            'timestamp': '',
            'data': {'message_id': '25d55ad283aa400af464c76d713c07ad'}
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_POST(self):
        print(self.headers)
        print(self.command)
        req_datas = self.rfile.read(int(self.headers['content-length'])) #重点在此步!
        print("req_datas is : %s" % req_datas.decode())

        testImage = Image.open(req_datas.decode())
        testImage = testImage.convert('L')
        testImage = testImage.resize((28, 28))
        img = (np.expand_dims(testImage,0))
        img = img / 255.0
        result = model.predict(img)
        print(np.argmax(result[0]))
        data = {
            'result_code': '1',
            'result_desc': 'Success',
            'timestamp': str(time.time()),
            'data': {'predict_result': str(np.argmax(result[0])) }
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

def _init_module():
    file_handle, pathname, desc = None, None, None
    file_handle, pathname, desc = imp.find_module("tensorflow", pathname)
    imp.load_module("tensorflow", file_handle, pathname, desc)
    file_handle, pathname, desc = None, None, None
    file_handle, pathname, desc = imp.find_module("numpy", pathname)
    imp.load_module("numpy", file_handle, pathname, desc)

model = tf.keras.models.load_model('model/mnist')


if __name__ == '__main__':
#    _init_module()
    host = ('', 9002)
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
    
