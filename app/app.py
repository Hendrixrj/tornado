from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import ujson as json
import logging
import requests
import json
import os
import sys

VERSION = '0.0.47'
CONTAINER_URI = '/containers/tests__tornado'

def print_stdout(message):

    logger = logging.getLogger(' TornadoApp ')
    logger.setLevel(logging.INFO)

    consolehandler = logging.StreamHandler(sys.stdout)
    consolehandler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    consolehandler.setFormatter(formatter)

    logger.addHandler(consolehandler)
    logger.info(message)

class Ping(tornado.web.RequestHandler):
    def get(self):
        response = {'get': 'ok'}
        self.write(response)

    def post(self):
        response = {'post': 'ok'}
        self.write(response)

    def put(self):
        response = {'put': 'ok'}
        self.write(response)

    def delete(self):
        response = {'delete': 'ok'}
        self.write(response)

class Version(tornado.web.RequestHandler):
    def get(self):
        response = {'version': VERSION}
        self.write(response)
 

# BigQueue Routes
class ProcessMessage(tornado.web.RequestHandler):
    '''
        Consume message from BigQueue.

    '''    
    def post(self):
        info = json.loads(self.request.body)
        response = {'success':  'ok', 'message': info}

        print_stdout(' Consume Queue - Info: ' + str(info))

        self.write(response)

class SendQueue(tornado.web.RequestHandler):
    '''
        Publish message in BigQueue.

    '''    
    def get(self):
        topic_name = os.environ['BIGQUEUE_TOPIC_TOPIC_TORNADO_TOPIC_NAME']
        endpoint = os.environ['BIGQUEUE_TOPIC_TOPIC_TORNADO_ENDPOINT']
        cluster_name = os.environ['BIGQUEUE_TOPIC_TOPIC_TORNADO_CLUSTER_NAME']

        json_data = {
            "msg": "teste", 
            "topics": [topic_name]
        }

        headers = {'content-type': 'application/json'}

        bigqueue_endpoint = "http://" + endpoint + "/messages"

        print_stdout(' Publish Queue ');
        try:
            r = requests.post(bigqueue_endpoint, data=json.dumps(json_data), headers=headers)
            stdout(r.text)
            self.write('ok \n {}'.format(r.text))
        except Exception as e:
            self.write('error:{}'.format(e))

# KVS Routes
class GetMessage(tornado.web.RequestHandler):
    '''
        Get key/value in KVS.

        Status Code expected : 200

    '''
    def get(self):
        endpoint_kvs_read = os.environ['KEY_VALUE_STORE_TESTS_END_POINT_READ'] + CONTAINER_URI + "/checklist"
        headers = {'Cntent-Type': 'application/json'}

        print_stdout(' Consume Message ');
        try:
            r = requests.get(endpoint_kvs_read, headers=headers)
            self.write('ok \n {}{}'.format(r.text, r.status_code))
        except Exception as e:
            stdout(e)
            self.write('error:{}'.format(e))

class SendMessage(tornado.web.RequestHandler):
    '''
        Send Json with key/value for KVS.

        Status Code expected : 201

    '''
    def get(self):
        endpoint_kvs_write = os.environ['KEY_VALUE_STORE_TESTS_END_POINT_WRITE'] + CONTAINER_URI
        headers = {'Content-Type': 'application/json'}

        json_data = {
        'key': 'checklist',
        'value': json.dumps({
               'checklist': {
                   "01": False,
               }
            })
        }
        
        print_stdout(' Publish Message ');
        try:
            r = requests.post(endpoint_kvs_write, json=json_data, headers=headers)
            
            self.write('ok \n {}{}'.format(r.text, r.status_code))
        except Exception as e:
            stdout(e)
            self.write('error:{}'.format(e))

  
application = tornado.web.Application([
    (r"/ping", Ping),
    (r"/version", Version),
    (r"/sendqueue", SendQueue),
    (r"/process", ProcessMessage),
    (r"/sendkvs", SendMessage),
    (r"/getkvs", GetMessage)


], debug=True)
 
if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()